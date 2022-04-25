OPKG_UTILS_VERSION = opkg-utils-0.5.0
OPKG_UTILS_URL = https://git.yoctoproject.org/opkg-utils/snapshot/$(OPKG_UTILS_VERSION).zip
OPKG_UTILS_PATH = build/$(OPKG_UTILS_VERSION)

all: | build
	@python3 ./fetch-and-validate.py ${TOKEN}
	$(OPKG_UTILS_PATH)/opkg-make-index build/packages > build/packages/Packages
	gzip -c build/packages/Packages > build/packages/Packages.gz

build:
	mkdir -p build
	mkdir -p build/packages
	wget -P build/ $(OPKG_UTILS_URL)
	unzip build/*.zip -d ./build

clean:
	rm -rf ./build

.Phony: all
