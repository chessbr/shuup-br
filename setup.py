import setuptools


if __name__ == '__main__':
    setuptools.setup(
        name="shoop-br",
        version="0.1.0",
        description="A Shoop add-on for custom Brazilian e-commerces",
        packages=["shoop_br"],
        include_package_data=True,
        entry_points={"shoop.addon": "shoop_br=shoop_br"}
    )