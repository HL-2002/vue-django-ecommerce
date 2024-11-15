export type Product = {
  id:                   number;
  title:                string;
  description:          string;
  category:             string;
  price:                number;
  discountPercentage:   number;
  rating:               number;
  stock:                number;
  tags:                 string[];
  brand:                string;
  sku:                  string;
  weight:               number;
  dimensions:           Dimensions;
  warrantyInformation:  string;
  shippingInformation:  string;
  availabilityStatus:   string;
  reviews:              Review[];
  returnPolicy:         string;
  minimumOrderQuantity: number;
  meta:                 Meta;
  images:               string[];
  thumbnail:            string;
}

export type Dimensions = {
  width:  number;
  height: number;
  depth:  number;
}

export type Meta = {
  id:number
  createdAt: string;
  updatedAt: string;
  barcode:   string;
  qrCode:    string;
}

export type Review = {
  rating:        number;
  comment:       string;
  date:          Date;
  reviewerName:  string;
  reviewerEmail: string;
}

export type Category = {
  id:   number;
  name: string;
}

export type Tag =  Category


export type SimplifiedProduct = Omit<Product, 'meta' | 'reviews'| "id"> & {
  meta: Omit<Meta, 'createdAt' | 'updatedAt' | 'qrCode'>;
}

export type NotificationType =  'error' | 'success';


export type NotificationSooner = {
  message: string;
  type:  NotificationType
}
