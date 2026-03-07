from setuptools import find_packages, setup

package_name = 'antenna_tracker'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mt',
    maintainer_email='mt@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'rssi_tracker = antenna_tracker.rssi_tracker:main',
            'gps_tracker = antenna_tracker.gps_tracker:main',
            'dummy = antenna_tracker.dummy:main',
            'rssi = antenna_tracker.rssi:main'
        ],
    },
)
