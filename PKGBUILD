# Maintainer: Lars Hagström <lars@foldspace.nu>
pkgname=disable-bd-prochot
pkgver=0.1
pkgrel=1
pkgdesc="A script that automatically disables the BD PROCHOT processor flag whenever it is turned on. This solved the problem where some Thinkpads go into extremely low CPU frequency when running on battery."
arch=('any')
license=('GPL')
depends=('python-lockfile' 'python-daemon')
makedepends=()
conflicts=()
replaces=()
backup=()
install=
source=('disable-bd-prochot' 'disable-bd-prochot.service')
sha256sums=('cc7479ac7f746d5a96520158b2e5144b59c0de86ed04d0d9625ca7106af7ad5e'
            'd591986f82b4576fa491b926f5fde8f5dfaa80c61eaf3b0e7ea37b6f8687b23f')
package() {
  install -D -m 555 "$srcdir/disable-bd-prochot" -t "$pkgdir/usr/bin/"
  install -D -m 555 "$srcdir/disable-bd-prochot.service" -t "$pkgdir/usr/lib/systemd/system/"
}
