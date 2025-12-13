from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aspect import Aspect
    from ..models.image import Image


T = TypeVar("T", bound="Product")


@_attrs_define
class Product:
    """This type contains the full details of a specified product, including information about the product's identifiers,
    product images, aspects, and categories.

        Attributes:
            additional_images (list[Image] | Unset): Contains information about  additional images associated with this
                product. For the primary image, see the <b>image</b> container.
            aspects (list[Aspect] | Unset): Contains an array of the category aspects and their values that are associated
                with this product.
            brand (str | Unset): The manufacturer's brand name for this product.
            compatibility_count (int | Unset): The number of distinct motor vehicles that are compatible with the
                product.<br><br>This field is only applicable for and will only be returned for Parts & Accessory products on
                the eBay US Motors marketplace.
            description (str | Unset): The rich description of this product, which might contain HTML.
            ean (list[str] | Unset): A list of all European Article Numbers (EANs) that identify this product.
            epid (str | Unset): The eBay product ID of this product.
            gtin (list[str] | Unset): A list of all GTINs that identify this product. Currently this can include EAN, ISBN,
                and UPC identifier types.
            image (Image | Unset): This type contains information about a product image stored in eBay Picture Services
                (EPS).
            isbn (list[str] | Unset): A list of all International Standard Book Numbers (ISBNs) that identify this product.
            mpn (list[str] | Unset): A list of all MPN values that the manufacturer uses to identify this product.
            other_applicable_category_ids (list[str] | Unset): A list of category IDs (other than the value of
                <b>primaryCategoryId</b>) for all the leaf categories to which this product might belong.
            primary_category_id (str | Unset): The identifier of the leaf category that eBay recommends using to list this
                product, based on previous listings of similar products. Products in the eBay catalog are not automatically
                associated with any particular category, but using an inappropriate category can make it difficult for
                prospective buyers to find the product. For other possible categories that might be used, see
                <b>otherApplicableCategoryIds</b>.
            product_web_url (str | Unset): The URL for this product's eBay product page.
            title (str | Unset): The title of this product on eBay.
            upc (list[str] | Unset): A list of Universal Product Codes (UPCs) that identify this product.
            version (str | Unset): The current version number of this product record in the catalog.
    """

    additional_images: list[Image] | Unset = UNSET
    aspects: list[Aspect] | Unset = UNSET
    brand: str | Unset = UNSET
    compatibility_count: int | Unset = UNSET
    description: str | Unset = UNSET
    ean: list[str] | Unset = UNSET
    epid: str | Unset = UNSET
    gtin: list[str] | Unset = UNSET
    image: Image | Unset = UNSET
    isbn: list[str] | Unset = UNSET
    mpn: list[str] | Unset = UNSET
    other_applicable_category_ids: list[str] | Unset = UNSET
    primary_category_id: str | Unset = UNSET
    product_web_url: str | Unset = UNSET
    title: str | Unset = UNSET
    upc: list[str] | Unset = UNSET
    version: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        additional_images: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.additional_images, Unset):
            additional_images = []
            for additional_images_item_data in self.additional_images:
                additional_images_item = additional_images_item_data.to_dict()
                additional_images.append(additional_images_item)

        aspects: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.aspects, Unset):
            aspects = []
            for aspects_item_data in self.aspects:
                aspects_item = aspects_item_data.to_dict()
                aspects.append(aspects_item)

        brand = self.brand

        compatibility_count = self.compatibility_count

        description = self.description

        ean: list[str] | Unset = UNSET
        if not isinstance(self.ean, Unset):
            ean = self.ean

        epid = self.epid

        gtin: list[str] | Unset = UNSET
        if not isinstance(self.gtin, Unset):
            gtin = self.gtin

        image: dict[str, Any] | Unset = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        isbn: list[str] | Unset = UNSET
        if not isinstance(self.isbn, Unset):
            isbn = self.isbn

        mpn: list[str] | Unset = UNSET
        if not isinstance(self.mpn, Unset):
            mpn = self.mpn

        other_applicable_category_ids: list[str] | Unset = UNSET
        if not isinstance(self.other_applicable_category_ids, Unset):
            other_applicable_category_ids = self.other_applicable_category_ids

        primary_category_id = self.primary_category_id

        product_web_url = self.product_web_url

        title = self.title

        upc: list[str] | Unset = UNSET
        if not isinstance(self.upc, Unset):
            upc = self.upc

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if additional_images is not UNSET:
            field_dict["additionalImages"] = additional_images
        if aspects is not UNSET:
            field_dict["aspects"] = aspects
        if brand is not UNSET:
            field_dict["brand"] = brand
        if compatibility_count is not UNSET:
            field_dict["compatibilityCount"] = compatibility_count
        if description is not UNSET:
            field_dict["description"] = description
        if ean is not UNSET:
            field_dict["ean"] = ean
        if epid is not UNSET:
            field_dict["epid"] = epid
        if gtin is not UNSET:
            field_dict["gtin"] = gtin
        if image is not UNSET:
            field_dict["image"] = image
        if isbn is not UNSET:
            field_dict["isbn"] = isbn
        if mpn is not UNSET:
            field_dict["mpn"] = mpn
        if other_applicable_category_ids is not UNSET:
            field_dict["otherApplicableCategoryIds"] = other_applicable_category_ids
        if primary_category_id is not UNSET:
            field_dict["primaryCategoryId"] = primary_category_id
        if product_web_url is not UNSET:
            field_dict["productWebUrl"] = product_web_url
        if title is not UNSET:
            field_dict["title"] = title
        if upc is not UNSET:
            field_dict["upc"] = upc
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aspect import Aspect
        from ..models.image import Image

        d = dict(src_dict)
        _additional_images = d.pop("additionalImages", UNSET)
        additional_images: list[Image] | Unset = UNSET
        if _additional_images is not UNSET:
            additional_images = []
            for additional_images_item_data in _additional_images:
                additional_images_item = Image.from_dict(additional_images_item_data)

                additional_images.append(additional_images_item)

        _aspects = d.pop("aspects", UNSET)
        aspects: list[Aspect] | Unset = UNSET
        if _aspects is not UNSET:
            aspects = []
            for aspects_item_data in _aspects:
                aspects_item = Aspect.from_dict(aspects_item_data)

                aspects.append(aspects_item)

        brand = d.pop("brand", UNSET)

        compatibility_count = d.pop("compatibilityCount", UNSET)

        description = d.pop("description", UNSET)

        ean = cast(list[str], d.pop("ean", UNSET))

        epid = d.pop("epid", UNSET)

        gtin = cast(list[str], d.pop("gtin", UNSET))

        _image = d.pop("image", UNSET)
        image: Image | Unset
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = Image.from_dict(_image)

        isbn = cast(list[str], d.pop("isbn", UNSET))

        mpn = cast(list[str], d.pop("mpn", UNSET))

        other_applicable_category_ids = cast(list[str], d.pop("otherApplicableCategoryIds", UNSET))

        primary_category_id = d.pop("primaryCategoryId", UNSET)

        product_web_url = d.pop("productWebUrl", UNSET)

        title = d.pop("title", UNSET)

        upc = cast(list[str], d.pop("upc", UNSET))

        version = d.pop("version", UNSET)

        product = cls(
            additional_images=additional_images,
            aspects=aspects,
            brand=brand,
            compatibility_count=compatibility_count,
            description=description,
            ean=ean,
            epid=epid,
            gtin=gtin,
            image=image,
            isbn=isbn,
            mpn=mpn,
            other_applicable_category_ids=other_applicable_category_ids,
            primary_category_id=primary_category_id,
            product_web_url=product_web_url,
            title=title,
            upc=upc,
            version=version,
        )

        product.additional_properties = d
        return product

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
