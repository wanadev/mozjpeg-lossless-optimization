import nox


PYTHON_FILES = [
    "mozjpeg_lossless_optimization",
    "tests",
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


@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"], reuse_venv=True)
def test(session):
    session.install("pytest")
    session.install(".")
    session.run("pytest", "-v", "tests")


@nox.session(reuse_venv=True)
def black_fix(session):
    session.install("black")
    session.run("black", *PYTHON_FILES)
