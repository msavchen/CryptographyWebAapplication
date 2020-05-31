from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from .forms import (
    MacForm,
    KeyGenForm,
    HashForm,
    EncryptForm,
    DecryptForm,
    EncryptFileForm,
)
from .rabbitMQ import CyperRpcClient


def mac(request):
    if request.method == "POST":
        macForm = MacForm(request.POST)
        keyForm = KeyGenForm(request.POST)
        if macForm.is_valid() and keyForm.is_valid():
            keySize = keyForm.cleaned_data["keyBitSize"]
            keyAlgo = keyForm.cleaned_data["keyAlgorithm"]

            plain = macForm.cleaned_data["plain"]
            algo = macForm.cleaned_data["algorithm"]

            cyberRcp = CyperRpcClient()
            response = cyberRcp.call("KEY," + keyAlgo + "," + keySize)
            keyForm = KeyGenForm(
                initial={
                    "keyBitSize": keySize,
                    "keyAlgorithm": keyAlgo,
                    "key": response,
                }
            )

            response = cyberRcp.call("MAC," + algo + "," + plain)
            macForm = MacForm(
                initial={"algorithm": algo, "plain": plain, "cipher": response}
            )
    else:
        macForm = MacForm(initial={"algorithm": "HmacSHA256"})
        macForm.fields["cipher"].widget = forms.HiddenInput()
        keyForm = KeyGenForm(initial={"keyBitSize": 128, "keyAlgorithm": "AES"})
        keyForm.fields["key"].widget = forms.HiddenInput()
    return render(request, "mac.html", {"macForm": macForm, "keyForm": keyForm})


def key(request):
    if request.method == "POST":
        form = KeyGenForm(request.POST)
        if form.is_valid():
            algo = form.cleaned_data["keyAlgorithm"]
            size = form.cleaned_data["keyBitSize"]
            cyberRcp = CyperRpcClient()
            response = cyberRcp.call("KEY," + algo + "," + size)
            form = KeyGenForm(
                initial={"keyAlgorithm": algo, "keyBitSize": size, "key": response}
            )
    else:
        form = KeyGenForm(initial={"keyBitSize": 128, "keyAlgorithm": "AES"})
        form.fields["key"].widget = forms.HiddenInput()
    return render(request, "keyGenerator.html", {"form": form})


def hash(request):
    if request.method == "POST":
        form = HashForm(request.POST)
        if form.is_valid():
            algo = form.cleaned_data["hashAlgorithm"]
            plain = form.cleaned_data["plainToHash"]
            cyberRcp = CyperRpcClient()
            response = cyberRcp.call("HASH," + algo + "," + plain)
            form = HashForm(
                initial={"hashAlgorithm": algo, "plain": plain, "hashed": response}
            )
    else:
        form = HashForm(initial={"hashAlgorithm": "SHA-512"})
        form.fields["hashed"].widget = forms.HiddenInput()
    return render(request, "hash.html", {"form": form})


def encrypt(request):
    if request.method == "POST":
        encryptForm = EncryptForm(request.POST)
        keyForm = KeyGenForm(request.POST)
        if encryptForm.is_valid() and keyForm.is_valid():
            keySize = keyForm.cleaned_data["keyBitSize"]
            keyAlgo = keyForm.cleaned_data["keyAlgorithm"]

            plain = encryptForm.cleaned_data["plain"]
            algo = encryptForm.cleaned_data["algorithm"]

            cyberRcp = CyperRpcClient()
            response = cyberRcp.call("KEY," + keyAlgo + "," + keySize)

            keyForm = KeyGenForm(
                initial={
                    "keyBitSize": keySize,
                    "keyAlgorithm": keyAlgo,
                    "key": response,
                }
            )

            response = cyberRcp.call("ENC," + algo + "," + plain)
            encryptForm = EncryptForm(
                initial={"algorithm": algo, "plain": plain, "cipher": response}
            )
    else:
        encryptForm = EncryptForm(initial={"algorithm": "AES/ECB/PKCS5Padding"})
        encryptForm.fields["cipher"].widget = forms.HiddenInput()
        keyForm = KeyGenForm(initial={"keyBitSize": 128, "keyAlgorithm": "AES"})
        keyForm.fields["key"].widget = forms.HiddenInput()
    return render(
        request, "encrypt.html", {"encryptForm": encryptForm, "keyForm": keyForm}
    )


def decrypt(request):
    if request.method == "POST":
        decryptForm = DecryptForm(request.POST)
        if decryptForm.is_valid():
            keyAlgo = decryptForm.cleaned_data["keyAlgorithm"]
            cipher = decryptForm.cleaned_data["cipher"]
            algo = decryptForm.cleaned_data["algorithm"]
            key = decryptForm.cleaned_data["key"]

            cyberRcp = CyperRpcClient()
            # response = cyberRcp.call("DEKEY," + keyAlgo + "," + key)

            response = cyberRcp.call("DEC," + algo + "," + cipher)
            decryptForm = DecryptForm(
                initial={
                    "algorithm": algo,
                    "plain": response,
                    "cipher": cipher,
                    "key": key,
                    "keyAlgorithm": keyAlgo,
                }
            )
    else:
        decryptForm = DecryptForm(
            initial={"algorithm": "AES/ECB/PKCS5Padding", "keyAlgorithm": "AES"}
        )
        decryptForm.fields["plain"].widget = forms.HiddenInput()
    return render(request, "decrypt.html", {"decryptForm": decryptForm})


def encryptFile(request):
    if request.method == "POST":
        encryptFileForm = EncryptFileForm(request.POST, request.FILES)
        keyForm = KeyGenForm(request.POST)
        if keyForm.is_valid() and encryptFileForm.is_valid():
            print('enter')
            keySize = keyForm.cleaned_data["keyBitSize"]
            keyAlgo = keyForm.cleaned_data["keyAlgorithm"]

            algo = encryptFileForm.cleaned_data["algorithm"]
            fileToEncrypt = request.FILES["fileToEncrypt"]
            data = fileToEncrypt.read()

            cyberRcp = CyperRpcClient()
            response = cyberRcp.call("KEY," + keyAlgo + "," + keySize)

            keyForm = KeyGenForm(
                initial={
                    "keyBitSize": keySize,
                    "keyAlgorithm": keyAlgo,
                    "key": response,
                }
            )

            response = cyberRcp.call("ENC," + algo + "," + str(data))
            encryptFileForm = EncryptFileForm(
                initial={
                    "algorithm": algo,
                    "fileToEncrypt": fileToEncrypt,
                    "cipher": response,
                }
            )
            encryptFileForm.fields["cipher"].widget.attrs["cols"] = 160
            encryptFileForm.fields["cipher"].widget.attrs["rows"] = 2 + len(response) / 160
            if '_save' in request.POST:
                print('save')
                with open('encryptedFiles/file.py', 'w') as file:
                    file.write(response)
    else:
        encryptFileForm = EncryptFileForm(initial={"algorithm": "AES/ECB/PKCS5Padding"})
        encryptFileForm.fields["cipher"].widget = forms.HiddenInput()
        keyForm = KeyGenForm(initial={"keyBitSize": 128, "keyAlgorithm": "AES"})
        keyForm.fields["key"].widget = forms.HiddenInput()

    return render(
        request,
        "encryptFile.html",
        {"encryptFileForm": encryptFileForm, "keyForm": keyForm},
    )
