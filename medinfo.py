# Moon-Userbot - telegram userbot
# Copyright (C) 2020-present Moon Userbot Organization
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import asyncio
import requests
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.scripts import format_exc, format_module_help

BASE_URL = "https://api.fda.gov/drug/label.json"


def get_drug_info(drug):
    url = f"{BASE_URL}?search={drug}&limit=1"
    response = requests.get(url)
    data = response.json()["results"][0]

    drug_info = {
        "Warning": data.get("disclaimer", [""])[0],
        "Generic Name": data["openfda"].get("generic_name", [""])[0],
        "Brand Name": data["openfda"].get("brand_name", [""])[0],
        "Manufacturer": data["openfda"].get("manufacturer_name", [""])[0],
        "Drug Type": data["openfda"].get("product_type", [""])[0],
        "Route": data["openfda"].get("route", [""])[0],
        "Substance": data["openfda"].get("substance_name", [""])[0],
        "NDC": data["openfda"].get("product_ndc", [""])[0],
        "Package Label": data.get("package_label_principal_display_panel", [""])[0],
        "Indications & Use": data.get("indications_and_usage", [""])[0],
        "Dosage & Administration": data.get("dosage_and_administration", [""])[0],
        "Warnings": data.get("warnings", [""])[0],
    }

    return drug_info


def get_ingredient_info(drug):
    url = f"{BASE_URL}?search=active_ingredient:{drug}&limit=1"
    response = requests.get(url)
    data = response.json()["results"][0]

    ingredient_info = {
        "Warning": data.get("disclaimer", [""])[0],
        "Package Label": data.get("package_label_principal_display_panel", [""])[0],
        "Purpose": data.get("purpose", [""])[0],
        "Active Ingredients": data.get("active_ingredient", [""])[0],
        "Inactive Ingredients": data.get("inactive_ingredient", [""])[0],
        "Indications & Use": data.get("indications_and_usage", [""])[0],
        "Dosage & Administration": data.get("dosage_and_administration", [""])[0],
        "Storage & Handling": data.get("storage_and_handling", [""])[0],
        "Warnings": data.get("warnings", [""])[0],
    }

    return ingredient_info


@Client.on_message(filters.command("medinfo", prefix) & filters.me)
async def medinfo(_, message: Message):
    if len(message.command) < 2:
        return await message.edit_text(format_module_help("medinfo"))

    drug = message.text.split(maxsplit=1)[1]
    await message.edit_text(
        f"__Searching >> `{drug}`__", parse_mode=enums.ParseMode.MARKDOWN
    )

    try:
        drug_info = get_drug_info(drug)
        if not drug_info:
            return await message.edit_text("No information found for the given drug.")

        await message.edit_text(
            f"<b>Warning:</b>\n<code>Do not rely on openFDA/moonub to make decisions regarding medical care. While we make every effort to ensure that data is accurate, you should assume all results are unvalidated. Also make sure drugs are out of reach of childrens</code>"
        )
        await asyncio.sleep(3)

        general_details = "\n\n".join(
            f"{key}: {value}"
            for key, value in drug_info.items()
            if key
            in [
                "Generic Name",
                "Brand Name",
                "Manufacturer",
                "Drug Type",
                "Route",
                "Substance",
                "NDC",
                "Package Label",
            ]
        )
        detailed_info = "\n\n".join(
            f"{key}: {value}"
            for key, value in drug_info.items()
            if key in ["Indications & Use", "Dosage & Administration"]
        )
        warnings = "\n\n".join(
            f"{key}: {value}" for key, value in drug_info.items() if key in ["Warnings"]
        ).replace("Warnings:", "")
        response = f"<b>General Details</b>:\n{general_details}\n\n<b>Detailed Information</b>:\n{detailed_info}\n\n<b>Warnings</b>:{warnings}"
        await message.edit_text(response)
    except Exception as e:
        await message.edit_text(format_exc(e))


@Client.on_message(filters.command("druginfo", prefix) & filters.me)
async def druginfo(_, message: Message):
    if len(message.command) < 2:
        return await message.edit_text(format_module_help("medinfo"))

    drug = message.text.split(maxsplit=1)[1]
    await message.edit_text(
        f"__Searching >> `{drug}`__", parse_mode=enums.ParseMode.MARKDOWN
    )

    try:
        drug_info = get_ingredient_info(drug)
        if not drug_info:
            return await message.edit_text("No information found for the given drug.")

        await message.edit_text(
            f"<b>Warning:</b>\n<code>Do not rely on openFDA/moonub to make decisions regarding medical care. While we make every effort to ensure that data is accurate, you should assume all results are unvalidated. Also make sure drugs are out of reach of childrens</code>"
        )
        await asyncio.sleep(3)

        general_details = "\n\n".join(
            f"{key}: {value}"
            for key, value in drug_info.items()
            if key in ["Package Label"]
        )
        detailed_info = "\n\n".join(
            f"{key}: {value}"
            for key, value in drug_info.items()
            if key
            in [
                "Purpose",
                "Active Ingredients",
                "Inactive Ingredients",
                "Indications & Use",
                "Dosage & Administration",
                "Storage & Handling",
            ]
        )
        warnings = "\n\n".join(
            f"{key}: {value}" for key, value in drug_info.items() if key in ["Warnings"]
        ).replace("Warnings:", "")
        response = f"<b>General Details</b>:\n{general_details}\n\n<b>Detailed Information</b>:\n{detailed_info}\n\n<b>Warnings</b>:{warnings}"
        await message.edit_text(response)
    except Exception as e:
        await message.edit_text(format_exc(e))


modules_help["medinfo"] = {
    "medinfo [drug name]": "Search for medical information about a drug",
    "druginfo [drug name]": "Search for information about an active ingredient",
}