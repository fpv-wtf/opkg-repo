OPKG_UTILS_VERSION = opkg-utils-0.5.0
OPKG_UTILS_URL = https://git.yoctoproject.org/opkg-utils/snapshot/$(OPKG_UTILS_VERSION).tar.gz
OPKG_UTILS_PATH = build/$(OPKG_UTILS_VERSION)

all: build entware pigeon
	cp index.html build/packages/index.html

pigeon:
	@python3 ./fetch-and-validate.py ${TOKEN} --template ./package-list.html --target build/packages/pigeon --html build/packages/pigeon

	$(OPKG_UTILS_PATH)/opkg-make-index build/packages/pigeon > build/packages/pigeon/Packages
	gzip -c build/packages/pigeon/Packages > build/packages/pigeon/Packages.gz

	$(OPKG_UTILS_PATH)/opkg-make-index build/packages/pigeon-prerelease > build/packages/pigeon-prerelease/Packages
	gzip -c build/packages/pigeon-prerelease/Packages > build/packages/pigeon-prerelease/Packages.gz

build:
	mkdir -p build
	mkdir -p build/packages
	mkdir -p build/packages/pigeon
	mkdir -p build/packages/pigeon-prerelease
	wget -P build/ $(OPKG_UTILS_URL)
	tar xzf build/*.tar.gz -C ./build

entware: build
	cp -R entware-armv7sf-k3.2 build/packages/
	$(OPKG_UTILS_PATH)/opkg-make-index build/packages/entware-armv7sf-k3.2 | grep -v "Lost field" > build/packages/entware-armv7sf-k3.2/Packages
	gzip -c build/packages/entware-armv7sf-k3.2/Packages > build/packages/entware-armv7sf-k3.2/Packages.gz

entware-mirror:
	rm -rf entware-armv7sf-k3.2/*.ipk*
	lynx -listonly -nonumbers -dump https://bin.entware.net/armv7sf-k3.2/ > /tmp/entware-repo.txt
	grep -f entware-packages.txt /tmp/entware-repo.txt > /tmp/entware-download.txt
	cd entware-armv7sf-k3.2 &&\
	wget -i /tmp/entware-download.txt

clean:
	rm -rf ./build

.Phony: all