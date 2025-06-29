"""
src/data_types/base_types.py

This module defines the foundational TypedDict data structures used for representing
various entities and attributes related to products, users, brands, models, and related metadata.

These types provide strong typing with optional fields to accurately model the complex
and potentially partial JSON data structures encountered during parsing.

Author: Сh.Danil
Created: 2025-06-28
Last Modified: 2025-06-29
Version: 1.0.0
"""

from typing import(
    Any, 
    TypedDict, 
    Optional, 
    List
)


class DedicatedUrlModel(TypedDict, total=False):
    path: Optional[str]


class DedicatedUrl(TypedDict, total=False):
    model: Optional[DedicatedUrlModel]


class Features(TypedDict, total=False):
    badge: Optional[str]
    branding: Optional[str]
    company_name: Optional[str]
    contact_email: Optional[str]
    contact_phones: Optional[str]
    contact_skype: Optional[str]
    cover: Optional[str]
    dedicated_url: Optional[DedicatedUrl]
    description: Optional[str]
    extended_info_in_ad: Optional[str]
    label: Optional[str]
    location: Optional[str]
    logo: Optional[str]
    no_competitors_ads: Optional[bool]
    personal_manager: Optional[str]
    photo_gallery: Optional[str]
    site_link: Optional[str]
    social_links: Optional[str]
    statistics: Optional[str]
    dynamic_wallet_balance: Optional[float]
    wallet_balance: Optional[float]
    dynamic_ppv_discount: Optional[float]
    ppv_discount: Optional[float]
    work_time: Optional[str]
    dynamic_free_ads_limit: Optional[int]
    free_ads_limit: Optional[int]
    greeting_message: Optional[str]
    wallet_cashback: Optional[float]


class Business(TypedDict, total=False):
    business: Optional[bool]
    features: Optional[Features]


class TrackingInfo(TypedDict, total=False):
    name: Optional[str]
    value: Optional[Any]


class Image(TypedDict, total=False):
    id: Optional[int]
    width: Optional[int]
    height: Optional[int]
    is_main: Optional[bool]
    is_cv_image: Optional[bool]
    p_hash: Optional[str]
    thumbnail_url: Optional[str]
    thumbnail_webp_url: Optional[str]
    original_url: Optional[str]
    original_webp_url: Optional[str]


class ParamLink(TypedDict, total=False):
    is_bottom: Optional[bool]
    is_popular: Optional[bool]
    value_id: Optional[int]
    value: Optional[str]
    url: Optional[str]


class Param(TypedDict, total=False):
    id: Optional[int]
    name: Optional[str]
    value: Optional[str]
    value_id: Optional[int]
    links: Optional[List[ParamLink]]


class User(TypedDict, total=False):
    is_deleted: Optional[bool]
    user_hash: Optional[str]
    hidden_delete: Optional[bool]
    response_time: Optional[int]
    id: Optional[int]
    avatar: Optional[str]
    pro: Optional[bool]
    is_banned: Optional[bool]
    response_rate: Optional[int]
    username: Optional[str]
    response_info: Optional[str]


class ExtendedUser(User, total=False):
    business: Optional[Business]
    online: Optional[bool]
    last_visit_time: Optional[int]
    user_id: Optional[int]


class PageVisibilityInfo(TypedDict, total=False):
    is_show_page: Optional[bool]


class BaseAttributes(TypedDict, total=False):
    id: Optional[int]
    old_id: Optional[int]
    country_id: Optional[int]
    status_id: Optional[int]
    category_id: Optional[int]
    user_id: Optional[int]
    user_ids: Optional[List[int]]
    origin_user_id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    city: Optional[str]
    hide_phone: Optional[bool]
    hide_chat: Optional[bool]
    lat: Optional[float]
    lng: Optional[float]
    views: Optional[int]
    impressions: Optional[int]
    favorite_count: Optional[int]
    callers_count: Optional[int]
    writers_count: Optional[int]
    is_vip: Optional[bool]
    is_select: Optional[bool]
    is_premium: Optional[bool]
    is_negotiable: Optional[bool]
    price: Optional[int]
    old_price: Optional[int]
    currency: Optional[str]
    symbol: Optional[str]
    mobile: Optional[str]
    images: Optional[List[Image]]
    created_time: Optional[int]
    updated_time: Optional[int]
    city_id: Optional[int]
    can_free_push: Optional[bool]
    score_order: Optional[int]
    is_freedom: Optional[bool]
    response_type: Optional[int]
    campaign_show: Optional[bool]
    is_ppv: Optional[bool]
    price_type: Optional[int]
    national_price: Optional[int]
    national_old_price: Optional[int]
    is_identity: Optional[bool]
    url: Optional[str]


class BaseProductAttributes(TypedDict, total=False):
    background: Optional[str]
    city_alias: Optional[str]
    paid_features: Optional[List]
    paid_packages: Optional[List]
    last_push_up: Optional[int]
    ad_label: Optional[str]


class ProductDetails(BaseAttributes, total=False):
    params: Optional[List[Param]]
    is_hide_house_number: Optional[bool]
    is_favorite: Optional[bool]
    device_id: Optional[int]
    user: Optional[ExtendedUser]
    username: Optional[str]
    email: Optional[str]
    features: Optional[List]
    products: Optional[List]
    rejected_reason: Optional[str]

    is_private_ad: Optional[bool]
    page_visibility_info: Optional[PageVisibilityInfo]
    available_campaign_types: Optional[List[str]]
    campaign: Optional[List]
    is_paid_posting: Optional[bool]
    sourcePage: Optional[str]


class Model(TypedDict, total=False):
    id: Optional[int]
    name: Optional[str]
    url: Optional[str]


class Brand(TypedDict, total=False):
    id: Optional[int]
    name: Optional[str]
    ads_count: Optional[int]
    url: Optional[str]
    image: Optional[str]
    singular_name: Optional[str]


class Format(TypedDict, total=False):
    ads_count: Optional[int]