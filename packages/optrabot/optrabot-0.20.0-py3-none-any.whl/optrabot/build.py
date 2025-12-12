import subprocess


def build_with_frontend() -> None:
	"""
	Build the OptraBot but including the build of the frontend.
	"""
	try:
		# Schritt 1: Frontend-Build ausführen (React UI)
		print('Running frontend build...')
		subprocess.run(['npm', 'run', 'build'], check=True, cwd='./frontend')  # noqa: S607
		
		# Schritt 2: UV-Build ausführen
		print('Running UV build...')
		subprocess.run(['uv', 'build'], check=True)  # noqa: S607

		print('Build completed successfully!')
	except subprocess.CalledProcessError as e:
		print(f'Error during build: {e}')
		return