from setuptools import setup, find_packages

setup(
    name="erpnext-ondc-network-seller-gateway",
    version="1.0.0",
    description="ERPNext ONDC Seller Gateway: Beckn Protocol B2B/B2C Catalog Discovery, Order Ingestion, Logistics Handshake & Settlement.",
    author="Shyam Kumar Pandey",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
