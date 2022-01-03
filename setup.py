from setuptools import setup
setup(
    name='app',
    description='FastAPI app',
    install_requires=[
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pytest',
        'requests',
    ],
    scripts=['main.py','create_db.py']
)