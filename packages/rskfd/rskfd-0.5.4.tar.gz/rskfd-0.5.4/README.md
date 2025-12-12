# rskfd Package

## Description

This repository contains the rskfd package, which is a python package containing tools for instrument and data handling.
Data handling mainly focuses on reading writing I/Q files in publich R&S formats.
Instrument Control is only based on raw socket connections.

**Note:**
* Software is provided as is
* Package APIs are subject to change, so consider saving the version you're using
* This is not an official Rohde & Schwarz package / software / product

## Usage

TBD: A detailed documentation will follow ...


### Installing

Use pip install rskfd to install package

### Folder structure

Here's a folder structure for a Pandoc document:

```
rskfd/     # Root directory.
|- iq_data_handling/        # Folder contains classes/scripts to handle iq data (files).
|- remote_control/          # Folder contains classes/scripts to handle remote connections to measurement instruments.
|- signal_generation/       # Folder contains classes/scripts to generate signals.
|- helper/                  # Folder contains classes/scripts for additional tools not directly related to the above.

```

### Setup generic data

```yml
---
title: rskfd Python Package
author: Florian Ramian
rights:  tbd
language: en-US
tags: [document]
abstract: |
  rskfd package for instrument control and I/Q data handling.
---
```