from django import forms


class MacForm(forms.Form):
    CHOICES = [
        ("HmacMD5", "HmacMD5"),
        ("HmacSHA1", "HmacSHA1"),
        ("HmacSHA256", "HmacSHA256"),
    ]
    algorithm = forms.ChoiceField(
        label="Algorithm for text ecryption", widget=forms.RadioSelect, choices=CHOICES
    )
    plain = forms.CharField(label="Text to encrypt", max_length=100)
    cipher = forms.CharField(
        label="Encrypted text",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"size": "100"}),
    )


class KeyGenForm(forms.Form):
    algo_choice = [
        ("AES", "AES"),
        ("DES", "DES"),
        ("DESede", "DESede"),
        ("HmacSHA1", "HmacSHA1"),
        ("HmacSHA256", "HmacSHA256"),
    ]
    size_choice = [(128, 128), (192, 192), (256, 256)]

    keyAlgorithm = forms.ChoiceField(
        label="Algorithm for key ", widget=forms.RadioSelect, choices=algo_choice
    )
    keyBitSize = forms.CharField(
        label="Key size ",
        max_length=5,
        required=True,
        widget=forms.TextInput(attrs={"size": "5"}),
    )
    key = forms.CharField(
        label="Generated key ",
        max_length=130,
        required=False,
        widget=forms.TextInput(attrs={"size": "130"}),
    )


class HashForm(forms.Form):
    algo_choice = [
        ("MD2", "MD2"),
        ("MD5", "MD5"),
        ("SHA-1", "SHA-1"),
        ("SHA-256", "SHA-256"),
        ("SHA-384", "SHA-384"),
        ("SHA-512", "SHA-512"),
    ]
    hashAlgorithm = forms.ChoiceField(
        label="Algorithm for hashing", widget=forms.RadioSelect, choices=algo_choice
    )
    plainToHash = forms.CharField(label="Text for hashing", max_length=100)
    hashed = forms.CharField(
        label="Hashed text",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"size": "100"}),
    )


class EncryptForm(forms.Form):
    CHOICES = [
        ("AES/CBC/NoPadding", "AES/CBC/NoPadding"),
        ("AES/CBC/PKCS5Padding", "AES/CBC/PKCS5Padding"),
        ("AES/ECB/NoPadding", "AES/ECB/NoPadding"),
        ("AES/ECB/PKCS5Padding", "AES/ECB/PKCS5Padding"),
        ("DES/CBC/NoPadding", "DES/CBC/NoPadding"),
        ("DES/CBC/PKCS5Padding", "DES/CBC/PKCS5Padding"),
        ("DES/ECB/NoPadding", "DES/ECB/NoPadding"),
    ]
    algorithm = forms.ChoiceField(
        label="Algorithm for text encryption ",
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
    plain = forms.CharField(
        label="Text to encrypt",
        max_length=130,
        required=False,
        widget=forms.TextInput(attrs={"size": "130"}),
    )
    cipher = forms.CharField(
        label="Encrypted text    ",
        max_length=130,
        required=False,
        widget=forms.TextInput(attrs={"size": "130"}),
    )


class DecryptForm(forms.Form):
    CHOICES = [
        ("AES/CBC/NoPadding", "AES/CBC/NoPadding"),
        ("AES/CBC/PKCS5Padding", "AES/CBC/PKCS5Padding"),
        ("AES/ECB/NoPadding", "AES/ECB/NoPadding"),
        ("AES/ECB/PKCS5Padding", "AES/ECB/PKCS5Padding"),
        ("DES/CBC/NoPadding", "DES/CBC/NoPadding"),
        ("DES/CBC/PKCS5Padding", "DES/CBC/PKCS5Padding"),
        ("DES/ECB/NoPadding", "DES/ECB/NoPadding"),
    ]

    algo_choice = [
        ("AES", "AES"),
        ("DES", "DES"),
        ("DESede", "DESede"),
        ("HmacSHA1", "HmacSHA1"),
        ("HmacSHA256", "HmacSHA256"),
    ]

    keyAlgorithm = forms.ChoiceField(
        label="Algorithm for key", widget=forms.RadioSelect, choices=algo_choice
    )
    algorithm = forms.ChoiceField(
        label="Algorithm for text encryption", widget=forms.RadioSelect, choices=CHOICES
    )
    key = forms.CharField(
        label="Key", max_length=100, widget=forms.TextInput(attrs={"size": "100"})
    )
    cipher = forms.CharField(
        label="Text to decrypt",
        max_length=100,
        widget=forms.TextInput(attrs={"size": "100"}),
    )
    plain = forms.CharField(
        label="Decrypted text",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"size": "100"}),
    )


class EncryptFileForm(forms.Form):
    CHOICES = [
        ("AES/CBC/NoPadding", "AES/CBC/NoPadding"),
        ("AES/CBC/PKCS5Padding", "AES/CBC/PKCS5Padding"),
        ("AES/ECB/NoPadding", "AES/ECB/NoPadding"),
        ("AES/ECB/PKCS5Padding", "AES/ECB/PKCS5Padding"),
        ("DES/CBC/NoPadding", "DES/CBC/NoPadding"),
        ("DES/CBC/PKCS5Padding", "DES/CBC/PKCS5Padding"),
        ("DES/ECB/NoPadding", "DES/ECB/NoPadding"),
    ]
    algorithm = forms.ChoiceField(
        label="Algorithm for text encryption ",
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
    fileToEncrypt = forms.FileField(label="File")
    cipher = forms.CharField(
        label="Encrypted text ",
        max_length=200,
        required=False,
        widget=forms.Textarea(),
    )
    #fileDir = forms.FilePathField()
