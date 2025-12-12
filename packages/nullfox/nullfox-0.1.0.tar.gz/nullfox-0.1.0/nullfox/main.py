import sys
from .encrypt import encrypt_file, decrypt_file

def main():
    if len(sys.argv) < 5:
        print("Usage: nullfox <encrypt|decrypt> <input> <output> <key>")
        return

    action, infile, outfile, key = sys.argv[1:5]

    if action == "encrypt":
        encrypt_file(infile, outfile, key)
        print("Encrypted ✅")
    elif action == "decrypt":
        decrypt_file(infile, outfile, key)
        print("Decrypted ✅")
    else:
        print("Unknown action!")

if __name__ == "__main__":
    main()