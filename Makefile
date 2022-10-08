OPKG_UTILS_VERSION = opkg-utils-0.5.0
OPKG_UTILS_URL = https://git.yoctoproject.org/opkg-utils/snapshot/$(OPKG_UTILS_VERSION).tar.gz
OPKG_UTILS_PATH = build/$(OPKG_UTILS_VERSION)

all: build pigeon
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

clean:
	rm -rf ./build

.Phony: all
