"""Helper module for configuring template renderers with formatting and Jinja2 options."""

from typing import Any, Dict, Optional


class RendererConfigurator:
    """Configures template renderers with formatting and Jinja2 environment options.

    This class handles the configuration of EnhancedTemplateRenderer instances by:
    1. Merging YAML and hook-based Jinja2 environment options
    2. Applying formatter managers
    3. Monkey-patching the renderer creation process
    """

    @staticmethod
    def configure_renderer(
        enhanced_renderer,
        formatter_manager,
        template_config,
        hook_env_options: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Configure an EnhancedTemplateRenderer with formatting and environment options.

        This method monkey-patches the create_renderer method to inject both the
        formatter manager and Jinja2 environment options.

        Environment options precedence (highest to lowest):
        1. Hook method options (hook_env_options parameter)
        2. YAML configuration (jinja_env section in template_config)

        Args:
            enhanced_renderer: The EnhancedTemplateRenderer instance to configure
            formatter_manager: Optional FormatterManager instance for code formatting
            template_config: TemplateConfig containing YAML configuration
            hook_env_options: Optional dict of Jinja2 env options from hook method
        """
        original_create_renderer = enhanced_renderer.create_renderer

        # Merge YAML and hook options with proper precedence
        env_options = RendererConfigurator._merge_env_options(template_config, hook_env_options)

        def create_renderer_with_config(
            context,
            filters,
            dry_run: bool = False,
            manual_section_config: Dict[str, str] = None,
        ):
            renderer = original_create_renderer(
                context, filters, dry_run=dry_run, manual_section_config=manual_section_config
            )

            # Apply formatter if provided
            if formatter_manager:
                renderer.set_formatter_manager(formatter_manager)

            # Apply Jinja2 environment options if any
            if env_options:
                renderer.set_env_options(**env_options)

            return renderer

        enhanced_renderer.create_renderer = create_renderer_with_config

    @staticmethod
    def _merge_env_options(template_config, hook_env_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Merge YAML and hook environment options with proper precedence.

        Args:
            template_config: TemplateConfig containing YAML configuration
            hook_env_options: Optional dict of Jinja2 env options from hook method

        Returns:
            Merged dictionary with hook options taking precedence over YAML
        """
        env_options = {}

        # Start with YAML config (if available)
        if template_config and hasattr(template_config, "jinja_env_config"):
            env_options = template_config.jinja_env_config.copy()

        # Hook options override YAML options
        if hook_env_options:
            env_options.update(hook_env_options)

        return env_options
