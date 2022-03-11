import 'dart:convert';
import 'package:flutter/material.dart';
import 'dart:io';

// import Process Dart class
void main() {
  runApp(MyApp());
}
// Build a flutter UI with two buttons and two labelled TextFields.
// The first button should display the value of the first text field.
// The second button should display the value of the second text field.

class MyApp extends StatelessWidget {
  MyApp();

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage();

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _textController1 = TextEditingController();
  final _textController2 = TextEditingController();
  final _textController3 = TextEditingController();

  String crackedText = '';
  String encryptedText = '';
  String decryptedText = '';

  static const outputFile = "out.txt";

  void EncryptPlainText() {
    Process.run(
      'python3',
      [' RSA_Breaker-4-bit 2 ', _textController1.text],
    );

    _textController1.text = ReadOutputFile();
  }

  void DecryptCipherText() {
    Process.run(
      'python3',
      [' RSA_Breaker-4-bit 3 ', _textController1.text],
    );

    _textController2.text = ReadOutputFile();
  }

  void CrackCipherText() {
    Process.run(
      'python3',
      [' RSA_Breaker-4-bit.py 4 ', _textController1.text],
    );

    _textController3.text = ReadOutputFile();
  }

// Read a single value from a text file
  String ReadOutputFile() {
    String value = File('./assets/out.txt').readAsStringSync();
    return value;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('4-bit RSA Maker and Cracker'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          children: <Widget>[
            TextField(
              controller: _textController1,
              decoration: InputDecoration(
                hintText: 'Plain Text',
              ),
            ),
            TextField(
              controller: _textController2,
              decoration: InputDecoration(
                hintText: 'Cipher Text',
              ),
            ),
            TextField(
              controller: _textController3,
              decoration: InputDecoration(
                hintText: 'Cracked Text',
              ),
            ),
            RaisedButton(
              child: const Text('Encrypt'),
              onPressed: () {
                setState(() {
                  EncryptPlainText();
                });
              },
            ),
            RaisedButton(
              child: const Text('Decrypt'),
              onPressed: () {
                setState(() {
                  DecryptCipherText();
                });
              },
            ),
            RaisedButton(
                child: const Text('Crack'),
                onPressed: () {
                  setState(() {
                    CrackCipherText();
                  });
                }),
          ], // <Widget>[]
        ),
      ),
    );
  }
}
