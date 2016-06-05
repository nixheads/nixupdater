PREFIX ?= /usr
TARGET = nixcontrolcenter
ARCH= all
HOSTARCH=$(shell dpkg-architecture -qDEB_HOST_MULTIARCH)
VERSION = 1.0.1


deb:
	sed -i "/Version:/c\Version: $(VERSION)" debian/DEBIAN/control
	install -d debian/usr/bin
	install -d debian/usr/share/applications
	install -d debian/usr/share/pixmaps
	install -d debian/usr/share/nixupdater
	install -d debian/usr/share/nixupdater/icons
	install -m 755 usr/bin/nixupdater debian/usr/bin
	install -m 644 usr/share/applications/nixupdater.desktop debian/usr/share/applications/nixupdater.desktop
	install -m 644 usr/share/pixmaps/nixupdater.png debian/usr/share/pixmaps/nixupdater.png
	install -m 644 usr/share/nixupdater/nixupdater.py debian/usr/share/nixupdater/nixupdater.py
	install -m 644 usr/share/nixupdater/nix-cache-check.py debian/usr/share/nixupdater/nix-cache-check.py
	install -m 644 usr/share/nixupdater/icons/* debian/usr/share/nixupdater/icons



	fakeroot dpkg-deb --build debian $(TARGET)_$(VERSION)_$(ARCH).deb
	rm -rf debian/usr




all: deb
