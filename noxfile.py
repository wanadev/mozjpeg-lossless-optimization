import nox


PYTHON_FILES = [
    "mozjpeg_lossless_optimization",
    "setup.py",
    "noxfile.py",
]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("flake8", "black")
    session.run("flake8", *PYTHON_FILES)
    session.run(
        "black",
        "--check",
        "--diff",
        "--color",
        *PYTHON_FILES,
    )


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"], reuse_venv=True)
def test(session):
    session.install("pytest")
    session.install(".")
    session.run("pytest", "-v", "tests")
