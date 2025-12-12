# Richie site factory plugin for Tutor

This is a plugin to integrate multiple [Richie](https://richie.education/) sites, the learning portal CMS, with [Open edX](https://open.edx.org). The integration takes the form of a [Tutor](https://docs.tutor.overhang.io) plugin.

## Dependencies

You should have create your own Richie site factory, go to https://richie.education/docs/cookiecutter/ to know more about it.


## Installation

```bash
pip install tutor-contrib-richie-site-factory
tutor plugins enable richie-site-factory
```

Running the Richie plugin will require that you rebuild the "openedx" Docker image:

```bash
tutor config save
tutor images build openedx
```

This step is necessary to install the Richie connector app in edx-platform.

Then, the platform can be launched as usual with:

```bash
tutor local quickstart
```

This plugins allows to run multiple Richie instance sites. So you have to configure each site factory sites so each can be run inside Tutor.


## Gettting started

Once your Richie platform is up and running, you will quickly realize that your learning portal is empty. This is because you should first create the corresponding courses and organizations from inside Richie. To do so, start by creating a super user:

```bash
tutor local run richie python manage.py createsuperuser
```

You can then use the credentials you just created at http(s)://yourrichiehost/admin. In development, this is http://courses.local.overhang.io/admin.

Then, refer to the official [Richie documentation](https://richie.education/docs/quick-start) to learn how to create courses and organizations.

You may also want to fill your learning portal with a demo site -- but be careful not to run this command in production, as it will be difficult to get rid of the demo site afterwards:

```bash
# WARNING: do not attempt this in production!
tutor local run richie-<mysite> python manage.py create_demo_site --force
```


## Configuration

This Tutor plugin comes with a few configuration settings:

- `RICHIE_RELEASE_VERSION` (default: `"v1.27.1"`) - the default version of the demo site
- `RICHIE_HOST` (default: `"courses.{{ LMS_HOST }}"`) - the marketing domain name at which the Open edX will be configured
- `RICHIE_MYSQL_ROOT_USERNAME` - (default: `{{ MYSQL_ROOT_USERNAME }}`)
- `RICHIE_MYSQL_ROOT_PASSWORD` - (default: `{{ MYSQL_ROOT_PASSWORD }}`)

Other are per site, replace the {site} with the name of your site:

- `RICHIE_{site}_HOST` - (default: `{site}.{{ LMS_HOST }}`)
- `RICHIE_{site}_DOCKER_IMAGE` - (default: `{{ DOCKER_REGISTRY }}fundocker/richie-demo:{{ RICHIE_RELEASE_VERSION }}`)
- `RICHIE_{site}_BUCKET_NAME` - (default: `richie-{site}-uploads`)
- `RICHIE_{site}_MEDIA_BUCKET_NAME` - (default: `richie-{site}-media`)
- `RICHIE_{site}_ELASTICSEARCH_INDICES_PREFIX` - (default: `richie-{site}`)
- `RICHIE_{site}_CACHE_DEFAULT_BACKEND` - (default: `base.cache.RedisCacheWithFallback`)
- `RICHIE_{site}_CACHE_DEFAULT_LOCATION` - (default: `redis://{{ REDIS_HOST }}:{{ REDIS_PORT }}/2`)
- `RICHIE_{site}_CACHE_DEFAULT_OPTIONS` - (default: `{}`)
- `RICHIE_{site}_DJANGO_SETTINGS_MODULE` - (default: `{site}.settings`)
- `RICHIE_{site}_DJANGO_CONFIGURATION` - (default: `Production`)
- `RICHIE_{site}_DB_ENGINE` - (default: `django.db.backends.mysql`)
- `RICHIE_{site}_DB_HOST` - (default: `{{ MYSQL_HOST }}`)
- `RICHIE_{site}_DB_NAME` - (default: `richie_{site}`)
- `RICHIE_{site}_DB_PORT` - (default: `{{ MYSQL_PORT }}`)
- `RICHIE_{site}_DB_USER` - (default: `richie_{site}`)
- `RICHIE_{site}_MYSQL_INIT` - (default: `true`)
- `RICHIE_{site}_MYSQL_ROOT_USERNAME` - (default: `{{ RICHIE_MYSQL_ROOT_USERNAME }}`)
- `RICHIE_{site}_MYSQL_ROOT_PASSWORD` - (default: `{{ RICHIE_MYSQL_ROOT_PASSWORD }}`)
- `RICHIE_{site}_ELASTICSEARCH_HOST` - (default: `{{ ELASTICSEARCH_HOST }}`)
- `RICHIE_{site}_EDX_BASE_URL` - (default: `https://{{ LMS_HOST }}`)
- `RICHIE_{site}_EDX_JS_BACKEND` - (default: `openedx-hawthorn`)
- `RICHIE_{site}_AUTHENTICATION_BASE_URL` - (default: `https://{{ LMS_HOST }}`)
- `RICHIE_{site}_AUTHENTICATION_BACKEND` - (default: `openedx-hawthorn`)
- `RICHIE_{site}_OAUTH2_CLIENT_AUTHORIZED_PATH` - (default: `None`)

If you need to completely customize the production environment, you can use the Tutor patch `richie-{{site}}-production-env`.

These defaults should be enough for most users. To modify any one of them, run:

```bash
tutor config save --set RICHIE_SETTING_NAME=myvalue
```

For instance, to customize the domain name at which Richie will run:

```bash
tutor config save --set "RICHIE_HOST=mysubdomain.{{ LMS_HOST }}"
```


## Development

Bind-mount volume:

```bash
tutor dev bindmount richie /app/richie
```

Then, run a development server:

```bash
tutor dev runserver --volume=/app/richie richie
```

The Richie development server will be available at http://courses.local.overhang.io:8003.


## Troubleshooting

Do you need help with this plugin? Get in touch by opening a GitHub issue: https://github.com/fccn/tutor-contrib-richie-site-factory/issues/


## Release

1. Increase the version in __about.py file, eg. 18.2.0.
2. Open a PR and merge it.
3. Then create a Git Tag with for the same version, v18.2.0

```bash
git tag v18.2.0
git push origin v18.2.0
```

## License

This software is licensed under the terms of the [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html). It was originally developed by Overhang.io with a sponsorship of [France Université Numérique](https://github.com/openfun). Currently, it's maintained by [NAU - FCCN|FCT](https://github.com/fccn).

<a href="https://www.fun-mooc.fr">
    <img alt="France Université Numérique" src="https://www.fun-mooc.fr/static/richie/images/logo-en.svg" width="200px" />
</a>

<a href="www.nau.edu.pt">
    <img alt="NAU by FCT" src="https://nau-prod-richie-nau-static-assets.rgw.nau.fccn.pt/static/richie/images/logo_nau_by_fccn_fct.3bc3aeaa7201.svg" width="200px" />
</a>
