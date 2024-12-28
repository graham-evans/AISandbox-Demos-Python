# Python examples for AI Sandbox Server

## Introduction to Protobuf for Python

An excellent introduction can be found in the [tutorial on FreeCodeCamp](https://www.freecodecamp.org/news/googles-protocol-buffers-in-python/).

## Required Dependencies

To run these examples you will need to download and install two libraries:

| Library            | Used Version | Description                                                           | More Information                                                 |
|--------------------|--------------|-----------------------------------------------------------------------|------------------------------------------------------------------|
| protobuf           | 5.29.1       | Main Protobuf library from Google                                     | [Project link](https://protobuf.dev/)                            |
| delimited-protobuf | 1.0.0        | Adds the ability to read and write streams of delimited Protobuf data | [Github link](https://github.com/soulmachine/delimited-protobuf) |

These can both be found using the Conda package manager.

## Updating Protobuf definitions

With Python, Protobuf files need to be processed and converted into Python code before they can be used. Each example includes the *.proto* and *_pb2.py* files already processed, but to recreate these, follow these steps:

1. Download the *protoc* tool from the [Protobuf repository](https://protobuf.dev/downloads/).
2. Download the latest *.proto* files from the [AISandbox repository](https://github.com/graham-evans/AISandbox-Server/tree/main/src/main/proto).
3. Run the following command in the directory with the *.proto* file (where 'filename' is the name of the *.proto* file to process):

```commandline
protoc.exe -I=. --python_out=. filename.proto
```