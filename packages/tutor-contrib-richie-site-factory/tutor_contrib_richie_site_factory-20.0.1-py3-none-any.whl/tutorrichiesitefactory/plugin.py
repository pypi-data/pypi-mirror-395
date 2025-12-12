import os
from glob import glob

import click
import importlib_resources
from tutor import config as tutor_config
from tutor import env, hooks

from .__about__ import __version__

templates = str(importlib_resources.files(
    "tutorrichiesitefactory") / "templates")

tutor_root_config = tutor_config.get_user(os.environ["TUTOR_ROOT"])

richie_sites = tutor_root_config.get("RICHIE_SITES", [])
config_unique = {}
for site in richie_sites:
    config_unique = {
        **config_unique,
        **{
            f"RICHIE_{site}_HOOK_SECRET": "{{ 20|random_string }}",
            f"RICHIE_{site}_SECRET_KEY": "{{ 20|random_string }}",
            f"RICHIE_{site}_DB_PASSWORD": "{{ 12|random_string }}",
            f"RICHIE_{site}_COURSE_RUN_SYNC_SECRETS": "{{ 12|random_string }}",
            f"RICHIE_{site}_AWS_ACCESS_KEY_ID": "{{ 20|random_string }}",
            f"RICHIE_{site}_AWS_SECRET_ACCESS_KEY": "{{ 40|random_string }}",
            f"RICHIE_{site}_OAUTH2_CLIENT_ID": "{{ 20|random_string }}",
            f"RICHIE_{site}_OAUTH2_CLIENT_ID_DEV": "{{ 20|random_string }}",
            f"RICHIE_{site}_OAUTH2_CLIENT_SECRET": "{{ 20|random_string }}",
        },
    }

richie_site_default_variables = {}
for site in richie_sites:
    richie_site_default_variables = {
        **richie_site_default_variables,
        **{
            f"RICHIE_{site}_HOST": site + ".{{ LMS_HOST }}",
            f"RICHIE_{site}_DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}fundocker/richie-demo:{{ RICHIE_RELEASE_VERSION }}",
            f"RICHIE_{site}_BUCKET_NAME": f"richie-{site}-uploads",
            f"RICHIE_{site}_MEDIA_BUCKET_NAME": f"richie-{site}-media",
            f"RICHIE_{site}_ELASTICSEARCH_INDICES_PREFIX": f"richie-{site}",
            f"RICHIE_{site}_CACHE_DEFAULT_BACKEND": "base.cache.RedisCacheWithFallback",
            f"RICHIE_{site}_CACHE_DEFAULT_LOCATION": "redis://{{ REDIS_HOST }}:{{ REDIS_PORT }}/2",
            f"RICHIE_{site}_CACHE_DEFAULT_OPTIONS": "{}",
            f"RICHIE_{site}_DJANGO_SETTINGS_MODULE": f"{site}.settings",
            f"RICHIE_{site}_DJANGO_CONFIGURATION": "Production",
            f"RICHIE_{site}_DB_ENGINE": "django.db.backends.mysql",
            f"RICHIE_{site}_DB_HOST": "{{ MYSQL_HOST }}",
            f"RICHIE_{site}_DB_NAME": f"richie_{site}",
            f"RICHIE_{site}_DB_PORT": "{{ MYSQL_PORT }}",
            f"RICHIE_{site}_DB_USER": f"richie_{site}",
            f"RICHIE_{site}_MYSQL_INIT": True,
            f"RICHIE_{site}_MYSQL_ROOT_USERNAME": "{{ RICHIE_MYSQL_ROOT_USERNAME }}",
            f"RICHIE_{site}_MYSQL_ROOT_PASSWORD": "{{ RICHIE_MYSQL_ROOT_PASSWORD }}",
            f"RICHIE_{site}_ELASTICSEARCH_HOST": "{{ ELASTICSEARCH_HOST }}",
            f"RICHIE_{site}_EDX_BASE_URL": "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}",
            f"RICHIE_{site}_EDX_JS_BACKEND": "openedx-hawthorn",
            f"RICHIE_{site}_AUTHENTICATION_BASE_URL": "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}",
            f"RICHIE_{site}_AUTHENTICATION_BACKEND": "openedx-hawthorn",
            # "/oauth2/authorized/",
            f"RICHIE_{site}_OAUTH2_CLIENT_AUTHORIZED_PATH": None,
        },
    }

config = {
    "unique": config_unique,
    "defaults": {
        ** {
            "RICHIE_VERSION": __version__,
            "RICHIE_SITES": [],
            "RICHIE_RELEASE_VERSION": "1.27.1",
            "RICHIE_ADD_SECRET_GENERATOR": True,
            "RICHIE_MYSQL_ROOT_USERNAME": "{{ MYSQL_ROOT_USERNAME }}",
            "RICHIE_MYSQL_ROOT_PASSWORD": "{{ MYSQL_ROOT_PASSWORD }}",
        },
        **richie_site_default_variables,
    },
}

hooks.Filters.IMAGES_BUILD.add_item((
    "richie",
    ("plugins", "richie", "build", "richie"),
    "{{ RICHIE_DOCKER_IMAGE }}",
    (),
))

hooks.Filters.IMAGES_PULL.add_item((
    "richie",
    "{{ RICHIE_DOCKER_IMAGE }}",
))

hooks.Filters.IMAGES_PUSH.add_item((
    "richie",
    "{{ RICHIE_DOCKER_IMAGE }}",
))

# Create the templates folder for each site
for site in richie_sites:
    for template_file in glob(
        os.path.join(
            templates,
            "richie/**",
        ),
        recursive=True,
    ):
        template_file_rel_dest = os.path.relpath(
            template_file, templates + "/richie")
        if os.path.isdir(template_file):
            os.makedirs(
                f"env/plugins/richie/templates/richie-{site}/{template_file_rel_dest}",
                exist_ok=True,
            )
        if os.path.isfile(template_file):
            with open(template_file, "r", encoding="utf-8") as f:
                data = f.read()
                data = data.replace("{{site}}", site)
                with open(f"env/plugins/richie/templates/richie-{site}/{template_file_rel_dest}", "w", encoding="utf-8") as f:
                    f.write(data)

# Add the "templates" folder as a template root
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    os.path.join("env/plugins/richie/templates"),
)

# Render the "build" and "apps" folders
for site in richie_sites:
    hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
        [
            (f"richie-{site}/build", "plugins"),
            (f"richie-{site}/apps", "plugins"),
        ],
    )
# Load patches from files
for path in glob(
    os.path.join(
        importlib_resources.files("tutorrichiesitefactory") / "patches",
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )

# Copy the patches per Richie site
for site in richie_sites:
    os.makedirs(f"env/plugins/richie/patches/richie-{site}", exist_ok=True)
    for path in glob(
        os.path.join(
            importlib_resources.files(
                "tutorrichiesitefactory") / "patches_per_site",
            "*",
        )
    ):
        with open(path, "r", encoding="utf-8") as patch_file:
            data = patch_file.read()
            data = data.replace("{{site}}", site)
            patch_name = os.path.basename(path)
            with open(f"env/plugins/richie/patches/richie-{site}/{patch_name}", "w", encoding="utf-8") as patch_file_write:
                patch_file_write.write(data)

# Register the patches per site
for site in richie_sites:
    for path in glob(
        f"env/plugins/richie/patches/richie-{site}/*"
    ):
        with open(path, encoding="utf-8") as patch_file:
            hooks.Filters.ENV_PATCHES.add_item(
                (os.path.basename(path), patch_file.read())
            )

# Add configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (key, value)
        for key, value in config.get("defaults", {}).items()
    ]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (key, value)
        for key, value in config.get("unique", {}).items()
    ]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)


def set_init_script_per_site(site: str):
    """
    Set the init script for the given site.
    """
    init_file_path = os.path.join(templates, "richie", "tasks", "lms", "init")

    with open(init_file_path, "r", encoding="utf-8") as init_file:
        init_file_data = init_file.read()
        init_file_data = init_file_data.replace("{{site}}", site)
        with open(f"env/plugins/richie/templates/richie-{site}/tasks/lms/init", "w", encoding="utf-8") as init_file_write:
            init_file_write.write(init_file_data)


for site in richie_sites:
    set_init_script_per_site(site)

    hooks.Filters.CLI_DO_INIT_TASKS.add_items([
        (
            "mysql",
            env.read_template_file(f"richie-{site}", "tasks", "mysql", "init")
        ),
        (
            f"richie-{site}",
            env.read_template_file(f"richie-{site}", "tasks", "richie", "init")
        ),
        (
            "lms",
            env.read_template_file(f"richie-{site}", "tasks", "lms", "init")
        ),
    ])


def register_cli_do_commands(site: str):
    """
    Register the CLI do commands for the given site.
    """

    @click.command(name=f"richie-{site}-init")
    def richie_init() -> list[tuple[str, str]]:
        """
        Job to create a minimum site structure required by Richie.
        """
        return [
            (
                f"richie-{site}",
                f"echo 'Initialize richie-{site} with a minimum site structure...' && "
                "python manage.py richie_init && "
                "echo 'Done!';",
            ),
        ]
    hooks.Filters.CLI_DO_COMMANDS.add_item(richie_init)

    @click.command(name=f"richie-{site}-create-demo-site")
    def create_demo_site() -> list[tuple[str, str]]:
        """
        Job to create a demo site.
        """
        return [
            (
                f"richie-{site}",
                f"echo 'Initialize richie-{site} with a minimum site structure...' && "
                # "python manage.py flush --force && "
                "python manage.py create_demo_site --force && "
                "python manage.py bootstrap_elasticsearch && "
                "echo 'Done!';",
            ),
        ]
    hooks.Filters.CLI_DO_COMMANDS.add_item(create_demo_site)

    @click.command(name=f"richie-{site}-bootstrap-elasticsearch")
    def bootstrap_elasticsearch() -> list[tuple[str, str]]:
        """
        Job to reindex Richie site.
        """
        return [
            (
                f"richie-{site}",
                f"echo 'Initialize richie-{site} with a minimum site structure...' && "
                "python manage.py bootstrap_elasticsearch && "
                "echo 'Done!';",
            ),
        ]
    hooks.Filters.CLI_DO_COMMANDS.add_item(bootstrap_elasticsearch)


for site in richie_sites:
    register_cli_do_commands(site)
