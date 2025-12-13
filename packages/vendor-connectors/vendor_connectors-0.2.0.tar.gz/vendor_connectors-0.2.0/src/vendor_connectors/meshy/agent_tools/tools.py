"""Core tool implementations for mesh-toolkit.

This module contains the actual tool logic, independent of any agent framework.
Each tool is defined as a handler function + metadata, which providers then
wrap in their framework-specific format.

The tools here use MeshyClient to interact with the Meshy API.
"""

from __future__ import annotations

from vendor_connectors.meshy.agent_tools.base import (
    ParameterDefinition,
    ToolCategory,
    ToolDefinition,
    ToolResult,
    register_tool,
)

# =============================================================================
# Tool Handlers - The actual implementation logic
# =============================================================================


def handle_text3d_generate(
    prompt: str,
    art_style: str = "sculpture",
    negative_prompt: str = "",
    target_polycount: int = 15000,
    enable_pbr: bool = True,
) -> str:
    """Generate a 3D model from text description.

    Args:
        prompt: Detailed text description of the 3D model
        art_style: One of: realistic, sculpture, cartoon, low-poly
        negative_prompt: Things to avoid in the generation
        target_polycount: Target polygon count
        enable_pbr: Enable PBR materials

    Returns:
        JSON result with task_id and status
    """
    try:
        from vendor_connectors.meshy import text3d

        result = text3d.generate(
            prompt,
            art_style=art_style,
            negative_prompt=negative_prompt,
            target_polycount=target_polycount,
            enable_pbr=enable_pbr,
            wait=True,
        )

        return ToolResult(
            success=True,
            data={
                "id": result.id,
                "status": result.status.value,
                "model_url": result.model_urls.glb if result.model_urls else None,
                "thumbnail_url": result.thumbnail_url,
            },
            task_id=result.id,
        ).to_json()

    except Exception as e:
        return ToolResult(success=False, error=str(e)).to_json()


def handle_rig_model(
    model_id: str,
    wait: bool = True,
) -> str:
    """Add skeleton/rig to a static 3D model.

    Args:
        model_id: Task ID of the static model to rig
        wait: Whether to wait for completion (default True)

    Returns:
        JSON result with rigging task_id and status
    """
    try:
        from vendor_connectors.meshy import rigging

        result = rigging.rig(model_id, wait=wait)

        if wait:
            return ToolResult(
                success=True,
                data={
                    "status": result.status.value,
                    "message": "Rigging completed",
                },
                task_id=result.id,
            ).to_json()

        return ToolResult(
            success=True,
            data={
                "status": "pending",
                "message": "Rigging task submitted",
            },
            task_id=result,  # task_id string when wait=False
        ).to_json()

    except Exception as e:
        return ToolResult(success=False, error=str(e)).to_json()


def handle_apply_animation(
    model_id: str,
    animation_id: int,
    wait: bool = True,
) -> str:
    """Apply animation to a rigged model.

    Args:
        model_id: Task ID of the rigged model
        animation_id: Animation ID from the Meshy catalog (integer)
        wait: Whether to wait for completion (default True)

    Returns:
        JSON result with animation task_id
    """
    try:
        from vendor_connectors.meshy import animate

        result = animate.apply(model_id, int(animation_id), wait=wait)

        if wait:
            return ToolResult(
                success=True,
                data={
                    "status": result.status.value,
                    "message": "Animation completed",
                    "glb_url": result.animation_glb_url,
                },
                task_id=result.id,
            ).to_json()

        return ToolResult(
            success=True,
            data={
                "status": "pending",
                "message": "Animation task submitted",
            },
            task_id=result,  # task_id string when wait=False
        ).to_json()

    except Exception as e:
        return ToolResult(success=False, error=str(e)).to_json()


def handle_retexture_model(
    model_id: str,
    texture_prompt: str,
    enable_pbr: bool = True,
    wait: bool = True,
) -> str:
    """Apply new textures to an existing model.

    Args:
        model_id: Task ID of the model to retexture
        texture_prompt: Description of the new texture/appearance
        enable_pbr: Enable PBR materials
        wait: Whether to wait for completion (default True)

    Returns:
        JSON result with retexture task_id
    """
    try:
        from vendor_connectors.meshy import retexture

        result = retexture.apply(
            model_id,
            texture_prompt,
            enable_pbr=enable_pbr,
            wait=wait,
        )

        if wait:
            return ToolResult(
                success=True,
                data={
                    "status": result.status.value,
                    "message": "Retexture completed",
                    "model_url": getattr(result, "model_url", None),
                },
                task_id=result.id,
            ).to_json()

        return ToolResult(
            success=True,
            data={
                "status": "pending",
                "message": "Retexture task submitted",
            },
            task_id=result,  # task_id string when wait=False
        ).to_json()

    except Exception as e:
        return ToolResult(success=False, error=str(e)).to_json()


def handle_list_animations(
    category: str = "",
    limit: int = 50,
) -> str:
    """List available animations from the Meshy catalog.

    Args:
        category: Optional category filter (Fighting, WalkAndRun, etc.)
        limit: Maximum number of results

    Returns:
        JSON list of animations
    """
    try:
        from vendor_connectors.meshy.animations import ANIMATIONS

        animations = list(ANIMATIONS.values())

        if category:
            animations = [a for a in animations if category.lower() in a.category.lower()]

        results = []
        for anim in animations[:limit]:
            results.append(
                {
                    "id": anim.id,
                    "name": anim.name,
                    "category": anim.category,
                    "subcategory": anim.subcategory,
                }
            )

        return ToolResult(
            success=True,
            data={
                "count": len(results),
                "total": len(animations),
                "animations": results,
            },
        ).to_json()

    except Exception as e:
        return ToolResult(success=False, error=str(e)).to_json()


def handle_check_task_status(
    task_id: str,
    task_type: str = "text-to-3d",
) -> str:
    """Check status of a Meshy task.

    Args:
        task_id: The Meshy task ID
        task_type: Task type (text-to-3d, rigging, animation, retexture)

    Returns:
        JSON with task status and progress
    """
    try:
        from vendor_connectors.meshy import animate, retexture, rigging, text3d

        # Call the appropriate get function based on task type
        get_funcs = {
            "text-to-3d": text3d.get,
            "rigging": rigging.get,
            "animation": animate.get,
            "retexture": retexture.get,
        }

        get_func = get_funcs.get(task_type)
        if not get_func:
            return ToolResult(
                success=False,
                error=f"Unknown task type: {task_type}",
            ).to_json()

        result = get_func(task_id)
        status = result.status.value if hasattr(result.status, "value") else str(result.status)

        # Get model URL if available
        model_url = None
        if hasattr(result, "model_urls") and result.model_urls:
            model_url = result.model_urls.glb
        elif hasattr(result, "glb_url"):
            model_url = result.glb_url

        return ToolResult(
            success=True,
            data={
                "status": status,
                "progress": getattr(result, "progress", None),
                "model_url": model_url,
            },
            task_id=task_id,
        ).to_json()

    except Exception as e:
        return ToolResult(success=False, error=str(e)).to_json()


def handle_get_animation_by_id(
    animation_id: int,
) -> str:
    """Get details of a specific animation.

    Args:
        animation_id: The animation ID number

    Returns:
        JSON with animation details
    """
    try:
        from vendor_connectors.meshy.animations import ANIMATIONS

        if animation_id not in ANIMATIONS:
            return ToolResult(
                success=False,
                error=f"Animation ID {animation_id} not found",
            ).to_json()

        anim = ANIMATIONS[animation_id]

        return ToolResult(
            success=True,
            data={
                "id": anim.id,
                "name": anim.name,
                "category": anim.category,
                "subcategory": anim.subcategory,
                "preview_url": anim.preview_url,
            },
        ).to_json()

    except Exception as e:
        return ToolResult(success=False, error=str(e)).to_json()


# =============================================================================
# Tool Registration - Define metadata for each tool
# =============================================================================


def _register_all_tools():
    """Register all tool definitions."""

    register_tool(
        ToolDefinition(
            name="text3d_generate",
            description=(
                "Generate a 3D GLB model from a text description using Meshy AI. "
                "Provide a detailed prompt describing the model. Returns the model "
                "file paths and metadata on success."
            ),
            category=ToolCategory.GENERATION,
            parameters={
                "prompt": ParameterDefinition(
                    name="prompt",
                    description="Detailed text description of the 3D model to generate",
                    type=str,
                    required=True,
                ),
                "art_style": ParameterDefinition(
                    name="art_style",
                    description="Art style for the model",
                    type=str,
                    required=False,
                    default="sculpture",
                    enum_values=["realistic", "sculpture", "cartoon", "low-poly"],
                ),
                "negative_prompt": ParameterDefinition(
                    name="negative_prompt",
                    description="Things to avoid in the generation",
                    type=str,
                    required=False,
                    default="",
                ),
                "target_polycount": ParameterDefinition(
                    name="target_polycount",
                    description="Target polygon count for the model",
                    type=int,
                    required=False,
                    default=15000,
                ),
                "enable_pbr": ParameterDefinition(
                    name="enable_pbr",
                    description="Enable PBR (physically-based rendering) materials",
                    type=bool,
                    required=False,
                    default=True,
                ),
            },
            handler=handle_text3d_generate,
        )
    )

    register_tool(
        ToolDefinition(
            name="rig_model",
            description=(
                "Add a skeleton/rig to a static 3D model. This is required before "
                "you can apply animations. Takes the model's task ID and returns "
                "a new task ID for the rigging operation."
            ),
            category=ToolCategory.RIGGING,
            parameters={
                "model_id": ParameterDefinition(
                    name="model_id",
                    description="Task ID of the static model to rig",
                    type=str,
                    required=True,
                ),
                "wait": ParameterDefinition(
                    name="wait",
                    description="Wait for rigging to complete (default True)",
                    type=bool,
                    required=False,
                    default=True,
                ),
            },
            handler=handle_rig_model,
        )
    )

    register_tool(
        ToolDefinition(
            name="apply_animation",
            description=(
                "Apply an animation to a rigged 3D model. Use list_animations to "
                "see available animation IDs. The model must be rigged first."
            ),
            category=ToolCategory.ANIMATION,
            parameters={
                "model_id": ParameterDefinition(
                    name="model_id",
                    description="Task ID of the rigged model to animate",
                    type=str,
                    required=True,
                ),
                "animation_id": ParameterDefinition(
                    name="animation_id",
                    description="Animation ID from the Meshy catalog (use list_animations)",
                    type=int,
                    required=True,
                ),
                "wait": ParameterDefinition(
                    name="wait",
                    description="Wait for animation to complete (default True)",
                    type=bool,
                    required=False,
                    default=True,
                ),
            },
            handler=handle_apply_animation,
        )
    )

    register_tool(
        ToolDefinition(
            name="retexture_model",
            description=(
                "Apply new textures to an existing 3D model. Great for creating "
                "color variants or material changes without regenerating the mesh."
            ),
            category=ToolCategory.TEXTURING,
            parameters={
                "model_id": ParameterDefinition(
                    name="model_id",
                    description="Task ID of the model to retexture",
                    type=str,
                    required=True,
                ),
                "texture_prompt": ParameterDefinition(
                    name="texture_prompt",
                    description="Description of the new texture/appearance",
                    type=str,
                    required=True,
                ),
                "enable_pbr": ParameterDefinition(
                    name="enable_pbr",
                    description="Enable PBR (physically-based rendering) materials",
                    type=bool,
                    required=False,
                    default=True,
                ),
                "wait": ParameterDefinition(
                    name="wait",
                    description="Wait for retexturing to complete (default True)",
                    type=bool,
                    required=False,
                    default=True,
                ),
            },
            handler=handle_retexture_model,
        )
    )

    register_tool(
        ToolDefinition(
            name="list_animations",
            description=(
                "List available animations from the Meshy animation catalog. "
                "Optionally filter by category. Returns animation IDs and names "
                "that can be used with apply_animation."
            ),
            category=ToolCategory.UTILITY,
            parameters={
                "category": ParameterDefinition(
                    name="category",
                    description="Optional category filter (Fighting, WalkAndRun, Dancing, etc.)",
                    type=str,
                    required=False,
                    default="",
                ),
                "limit": ParameterDefinition(
                    name="limit",
                    description="Maximum number of animations to return",
                    type=int,
                    required=False,
                    default=50,
                ),
            },
            handler=handle_list_animations,
            requires_api_key=False,
        )
    )

    register_tool(
        ToolDefinition(
            name="check_task_status",
            description=(
                "Check the current status of a Meshy AI task. Returns status "
                "(pending, processing, succeeded, failed), progress percentage, "
                "and model URL if complete."
            ),
            category=ToolCategory.UTILITY,
            parameters={
                "task_id": ParameterDefinition(
                    name="task_id",
                    description="The Meshy task ID to check",
                    type=str,
                    required=True,
                ),
                "task_type": ParameterDefinition(
                    name="task_type",
                    description="Task type",
                    type=str,
                    required=False,
                    default="text-to-3d",
                    enum_values=["text-to-3d", "rigging", "animation", "retexture"],
                ),
            },
            handler=handle_check_task_status,
        )
    )

    register_tool(
        ToolDefinition(
            name="get_animation",
            description=(
                "Get details of a specific animation by ID, including name, category, subcategory, and preview URL."
            ),
            category=ToolCategory.UTILITY,
            parameters={
                "animation_id": ParameterDefinition(
                    name="animation_id",
                    description="The animation ID number",
                    type=int,
                    required=True,
                ),
            },
            handler=handle_get_animation_by_id,
            requires_api_key=False,
        )
    )


# Register tools on module import
_register_all_tools()
