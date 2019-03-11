# h-k-p-CoherenceVerifier 

Python script to verify h-k-p Coherence.

## Usage

These instructions will tell you how to use the verifier.

### Getting started

The script take two dataset as input. One dataset with only public items and one dataset with only private items.

### Running

Launch the script with two parameters:
* pub _filepath_ - the dataset with public items
* priv _filepath_ - the dataset with private items
* p - items known by attacker
* k - Minumun number of transactions
* h - Probability to deanonimize some item

Example

```
python3 verifier.py -pub dataset_pub.dat -priv dataset_priv.dat -p 4 -k 3 -p 0.8
```

The result will be print to console.

## Resource

* [Paper](https://www.cs.sfu.ca/~wangk/pub/kdd455-xu.pdf) - Anonymizing Transaction Databases for Publication

## Authors

* **Luigi Sciolla** - [github](https://github.com/Killuaa27)
* **Eugenio Polleri** - [github](https://github.com/eugep)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
