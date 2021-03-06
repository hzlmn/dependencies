from setuptools import setup


setup(name="helpers", py_modules=["helpers"])

setup(name="pkg", packages=["pkg", "pkg.circles"])

setup(
    name="django_project",
    packages=["django_project", "django_project.api"],
    include_package_data=True,
    package_data={"django_project": ["templates/*.html"]},
)

setup(name="flask_project", packages=["flask_project"])
