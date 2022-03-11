// @dart=2.15

import 'dart:ui' as ui;

import 'package:user_interface_for_rsa_breaker/main.dart' as entrypoint;

Future<void> main() async {
  await ui.webOnlyInitializePlatform();
  entrypoint.main();
}
