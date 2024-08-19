# Go Lava

This project was inspired by [LavaRand](https://www.lavarand.org/) and [Cloudflare's lava lamps](https://blog.cloudflare.com/lavarand-in-production-the-nitty-gritty-technical-details/). I did not look at any of their code, nor their approach, but thought it would be a fun Golang learning project to implement myself.

## How it works

With this utility, the user is prompted to select their own image. The tool will check to ensure the image is readable from the filesystem, and it will then generate a random string of characters based on the image's pixel data. From here, the user has the option to apply SHA256 hashing to the generated string, as well as set the length of the string to be generated.

## Usage

Run the script using the go run command:

```bash
go run main.go
```

1. You will be asked to supply an image. The path can be relative or absolute (it will check to ensure it can locate the file). I've included `test.jpg` in the repository for testing purposes.
2. Once the image is selected, you will be asked whether or not you want to hash the generated string (y/n).
3. You will also be asked to set the length of the string to be generated. As an aside, if you choose to hash the string, the length of the hash will be 64 characters (I provide a note when running the script).
4. That's it! The script will generate the string and output it to the console.
