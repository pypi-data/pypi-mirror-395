from typing import List, Optional, Union
from pydantic import BaseModel, Field, ValidationError
from dataclasses import dataclass
from producteca.abstract.abstract_dataclass import BaseService
from producteca.products.search_products import SearchProduct, SearchProductParams
from producteca.utils import clean_model_dump
import logging
import requests

_logger = logging.getLogger(__name__)


class Attribute(BaseModel):
    key: str
    value: str


class Tag(BaseModel):
    tag: str


class Dimensions(BaseModel):
    weight: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    length: Optional[float] = None
    pieces: Optional[int] = None


class Deal(BaseModel):
    campaign: str
    regular_price: Optional[float] = Field(default=None, alias='regularPrice')
    deal_price: Optional[float] = Field(default=None, alias='dealPrice')


class Stock(BaseModel):
    quantity: Optional[int] = None
    available_quantity: Optional[int] = Field(default=None, alias='availableQuantity')
    warehouse: Optional[str] = None
    warehouse_id: Optional[int] = Field(default=None, alias='warehouseId')
    reserved: Optional[int] = None
    available: Optional[int] = None


class Price(BaseModel):
    amount: Optional[float] = None
    currency: str
    price_list: str = Field(alias='priceList')
    price_list_id: Optional[int] = Field(default=None, alias='priceListId')


class Picture(BaseModel):
    url: str


class Integration(BaseModel):
    app: Optional[int] = None
    integration_id: Optional[str] = Field(default=None, alias='integrationId')
    permalink: Optional[str] = None
    status: Optional[str] = None
    listing_type: Optional[str] = Field(default=None, alias='listingType')
    safety_stock: Optional[int] = Field(default=None, alias='safetyStock')
    synchronize_stock: Optional[bool] = Field(default=None, alias='synchronizeStock')
    is_active: Optional[bool] = Field(default=None, alias='isActive')
    is_active_or_paused: Optional[bool] = Field(default=None, alias='isActiveOrPaused')
    id: Optional[int] = None
    parent_integration: Optional[str] = Field(default=None, alias='parentIntegration')


class Variation(BaseModel):
    variation_id: Optional[int] = Field(default=None, alias='variationId')
    components: Optional[List] = None
    pictures: Optional[Union[List[Picture], List]] = None
    stocks: Optional[Union[List[Stock], List]] = None
    attributes_hash: Optional[str] = Field(default=None, alias='attributesHash')
    primary_color: Optional[str] = Field(default=None, alias='primaryColor')
    thumbnail: Optional[str] = None
    attributes: Optional[Union[List[Attribute], List]] = None
    integrations: Optional[Union[List[Integration], List]] = None
    id: Optional[int] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None


class MeliCategory(BaseModel):
    meli_id: Optional[str] = Field(default=None, alias='meliId')
    accepts_mercadoenvios: Optional[bool] = Field(default=None, alias='acceptsMercadoenvios')
    suggest: Optional[bool] = None
    fixed: Optional[bool] = None


class BundleComponent(BaseModel):
    quantity: int
    variation_id: int = Field(alias='variationId')
    product_id: int = Field(alias='productId')


class BundleVariation(BaseModel):
    variation_id: int = Field(alias='variationId')
    components: Union[List[BundleComponent], List]


class BundleResult(BaseModel):
    company_id: int = Field(alias='companyId')
    product_id: int = Field(alias='productId')
    variations: Union[List[BundleVariation], List]
    id: str


class BundleResponse(BaseModel):
    results: Union[List[BundleResult], List]
    count: int


class Product(BaseModel):
    integrations: Optional[Union[List[Integration], List]] = None
    variations: Optional[Union[List[Variation], List]] = None
    is_simple: Optional[bool] = Field(default=None, alias='isSimple')
    has_variations: Optional[bool] = Field(default=None, alias='hasVariations') 
    thumbnail: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[str] = None
    prices: Optional[Union[List[Price], List]] = None
    buying_price: Optional[float] = Field(default=None, alias='buyingPrice')
    is_archived: Optional[bool] = Field(default=None, alias='isArchived')
    dimensions: Optional[Union[Dimensions, dict]] = None
    attributes: Optional[Union[List[Attribute], List]] = None
    metadata: Optional[List[str]] = None
    is_original: Optional[bool] = Field(default=None, alias='isOriginal')
    name: str
    code: Optional[str] = None
    sku: Optional[str] = None
    brand: Optional[str] = None
    id: Optional[int] = None


class ProductVariationBase(BaseModel):
    sku: str
    variation_id: Optional[int] = Field(default=None, alias='variationId')
    code: Optional[str] = None
    barcode: Optional[str] = None
    attributes: Union[List[Attribute], List] = []
    tags: Optional[List[str]] = []
    buying_price: Optional[float] = Field(default=None, alias='buyingPrice')
    dimensions: Optional[Union[Dimensions, dict]] = Field(default_factory=Dimensions)
    brand: Optional[str] = ''
    notes: Optional[str] = ''
    deals: Optional[Union[List[Deal], List]] = []
    stocks: Optional[Union[List[Stock], List]] = []
    prices: Optional[Union[List[Price], List]] = []
    pictures: Optional[Union[List[Picture], List]] = []


class ProductVariation(ProductVariationBase):
    category: Optional[str] = Field(default=None)
    name: Optional[str] = None


class Shipping(BaseModel):
    local_pickup: Optional[bool] = Field(default=None, alias='localPickup')
    mode: Optional[str] = None
    free_shipping: Optional[bool] = Field(default=None, alias='freeShipping')
    free_shipping_cost: Optional[float] = Field(default=None, alias='freeShippingCost')
    mandatory_free_shipping: Optional[bool] = Field(default=None, alias='mandatoryFreeShipping')
    free_shipping_method: Optional[str] = Field(default=None, alias='freeShippingMethod')


class MShopsShipping(BaseModel):
    enabled: Optional[bool] = None


class AttributeCompletion(BaseModel):
    product_identifier_status: Optional[str] = Field(default=None, alias='productIdentifierStatus')
    data_sheet_status: Optional[str] = Field(default=None, alias='dataSheetStatus')
    status: Optional[str] = None
    count: Optional[int] = None
    total: Optional[int] = None


class MeliProduct(BaseModel):
    product_id: Optional[int] = Field(default=None, alias='productId')
    tags: Optional[List[str]] = Field(default=None)
    has_custom_shipping_costs: Optional[bool] = Field(default=None, alias='hasCustomShippingCosts')
    shipping: Optional[Union[Shipping, dict]] = None
    mshops_shipping: Optional[Union[MShopsShipping, dict]] = Field(default=None, alias='mShopsShipping')
    add_free_shipping_cost_to_price: Optional[bool] = Field(default=None, alias='addFreeShippingCostToPrice')
    category: Union[MeliCategory, dict]
    attribute_completion: Optional[Union[AttributeCompletion, dict]] = Field(default=None, alias='attributeCompletion')
    catalog_products: Optional[List[str]] = Field(default=None, alias='catalogProducts')
    warranty: Optional[str] = None
    domain: Optional[str] = None
    listing_type_id: Optional[str] = Field(default=None, alias='listingTypeId')
    catalog_products_status: Optional[str] = Field(default=None, alias='catalogProductsStatus')


class ErrorMessage(BaseModel):
    en: str
    es: str
    pt: str


class ErrorReason(BaseModel):
    code: str
    error: str
    message: ErrorMessage
    data: Optional[dict] = None


class ResolvedValue(BaseModel):
    updated: bool


class ResolvedError(BaseModel):
    resolved: Optional[bool] = None
    reason: Optional[Union[ErrorReason, dict]] = None
    value: Optional[Union[ResolvedValue, dict]] = None
    statusCode: Optional[int] = None


class ErrorContext(BaseModel):
    _ns_name: str
    id: int
    requestId: str
    tokenAppId: str
    appId: str
    bearer: str
    eventId: str


class SynchronizeResponse(BaseModel):
    product: Optional[Union[ResolvedError, dict]] = None
    variation: Optional[Union[ResolvedError, dict]] = None
    deals: Optional[Union[ResolvedError, dict]] = None
    bundles: Optional[Union[ResolvedError, dict]] = None
    taxes: Optional[Union[ResolvedError, dict]] = None
    meliProductListingIntegrations: Optional[Union[ResolvedError, dict]] = None
    tags: Optional[Union[ResolvedError, dict]] = None
    productIntegrations: Optional[Union[ResolvedError, dict]] = None
    statusCode: Optional[int] = None
    error_context: Optional[Union[ErrorContext, dict]] = Field(None, alias='error@context')


class ListedSynchronizeResponse(BaseModel):
    results: Union[List[SynchronizeResponse], List]


@dataclass
class ProductService(BaseService):
    endpoint: str = 'products'
    create_if_it_doesnt_exist: bool = Field(default=False, exclude=True)

    def __call__(self, **payload):
        self._record = Product(**payload)
        return self

    def synchronize(self, payload) -> Union[Product, SynchronizeResponse]:
        endpoint_url = self.config.get_endpoint(f'{self.endpoint}/synchronize')
        headers = self.config.headers.copy()
        headers.update({"createifitdoesntexist": str(self.create_if_it_doesnt_exist).lower()})
        product_variation = ProductVariation(**payload)
        if not product_variation.code and not product_variation.sku:
            raise Exception("Sku or code should be provided to update the product")
        # Hacer model_dump con limpieza automática de valores vacíos
        data = clean_model_dump(product_variation)
        _logger.info(f"Synchronizing product: {data}")
        _logger.info(f"POST {endpoint_url} - Headers: {headers} - Data: {data}")
        response = requests.post(endpoint_url, json=data, headers=headers)
        if not response.ok:
            raise Exception(f"Error getting product {product_variation.sku} - {product_variation.code}\n {response.text}")
        if response.status_code == 204:
            _logger.info("Status code is 204 (No Content), product synchronized successfully but no changes were made")
            return None
        
        _logger.info(f"response text: {response.text}")
        response_data = response.json()
        _logger.debug(f"Response data: {response_data}")
        if isinstance(response_data, list):
            res = ListedSynchronizeResponse(results=response_data)
            if res.results and hasattr(res.results[0], 'error_context') and res.results[0].error_context:
                raise Exception(f"Errored while updating {res.results[0].error_context} {res.model_dump_json()}")
            return res.results[0] if res.results else None

        if isinstance(response_data, dict) and 'name' in response_data:
            return Product(**response_data)

        if isinstance(response_data, dict) and any(key in response_data for key in ['product', 'variation', 'statusCode']):
            sync_resp = SynchronizeResponse(**response_data)
            if sync_resp.error_context:
                raise Exception(f"Errored while updating {sync_resp.error_context} - {sync_resp.model_dump_json()}")
            return sync_resp

        if isinstance(response_data, dict) and 'message' in response_data:
            error_res = ErrorReason(**response_data)
            raise Exception(f"Errored with the following message {error_res.message} - {error_res.model_dump_json()}")
        
        raise Exception(f"Unhandled response format, check response {response.text}")

    def get(self, product_id: int) -> "ProductService":
        endpoint_url = self.config.get_endpoint(f'{self.endpoint}/{product_id}')
        headers = self.config.headers
        _logger.info(f"GET {endpoint_url} - Headers: {headers}")
        response = requests.get(endpoint_url, headers=headers)
        if not response.ok:
            raise Exception(f"Error getting product {product_id}\n {response.text}")
        response_data = response.json()
        return self(**response_data)

    def get_bundle(self, product_id: int) -> BundleResponse:
        endpoint_url = self.config.get_endpoint(f'{self.endpoint}/{product_id}/bundles')
        headers = self.config.headers
        _logger.info(f"GET {endpoint_url} - Headers: {headers}")
        response = requests.get(endpoint_url, headers=headers)
        if not response.ok:
            raise Exception(f"Error getting bundle {product_id}\n {response.text}")
        return BundleResponse(**response.json())

    def get_ml_integration(self, product_id: int) -> MeliProduct:
        endpoint_url = self.config.get_endpoint(f'{self.endpoint}/{product_id}/listingintegration')
        headers = self.config.headers
        _logger.info(f"GET {endpoint_url} - Headers: {headers}")
        response = requests.get(endpoint_url, headers=headers)
        if not response.ok:
            raise Exception(f"Error getting ml integration {product_id}\n {response.text}")
        response_data = response.json()
        return MeliProduct(**response_data)

    def search(self, params: SearchProductParams) -> SearchProduct:
        endpoint: str = f'search/{self.endpoint}'
        headers = self.config.headers
        url = self.config.get_endpoint(endpoint)
        params_dict = clean_model_dump(params)
        _logger.info(f"GET {url} - Headers: {headers} - Params: {params_dict}")
        response = requests.get(url, headers=headers, params=params_dict)
        _logger.info(f"Response status: {response.status_code} - Response text: {response.text}")
        if not response.ok:
            raise Exception(f"error in searching products {response.text}")
        return SearchProduct(**response.json())
