package ru.ifmo.se.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DeliveryDto {
    @JsonProperty("delivery_id")
    private String deliveryId;
    @JsonProperty("order_id")
    private String orderId;
    @JsonProperty("order_date_created")
    private String orderDateCreated;
    @JsonProperty("deliveryman_id")
    private String deliveryManId;
    @JsonProperty("delivery_address")
    private String deliveryAddress;
    @JsonProperty("delivery_time")
    private String deliveryTime;
    @JsonProperty("rating")
    private int rating;
    @JsonProperty("tips")
    private int tips;
}
