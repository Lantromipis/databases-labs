package ru.ifmo.se;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import ru.ifmo.se.model.DeliveryDto;

import java.io.InputStream;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Path("/api/delivery")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class DeliveryResource {

    @Inject
    ObjectMapper objectMapper;

    DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"); //2024-05-21 12:18:22

    @GET
    public Response getDelivery(@QueryParam("limit") Integer limit,
                                @QueryParam("offset") Integer offset,
                                @QueryParam("delivery_time_gt") String deliveryTime) throws Exception {
        try (InputStream inputStream = this.getClass().getClassLoader().getResourceAsStream("delivery.json")) {
            List<DeliveryDto> dtos = objectMapper.readValue(inputStream, new TypeReference<List<DeliveryDto>>() {
            });

            if (deliveryTime != null) {
                LocalDateTime ldt = LocalDateTime.parse(deliveryTime, dtf);
                dtos = dtos.stream()
                        .filter(
                                d -> {
                                    LocalDateTime deliveryLocalDate = LocalDateTime.parse(d.getDeliveryTime(), dtf);
                                    return deliveryLocalDate.isAfter(ldt);
                                }
                        )
                        .toList();
            }

            if (limit == null && offset == null) {
                return Response.ok(dtos).build();
            }

            if (limit == null) {
                limit = 1;
            }
            if (offset == null) {
                offset = 0;
            }


            return Response
                    .ok(
                            dtos.stream()
                                    .skip(offset)
                                    .limit(limit)
                                    .toList()
                    )
                    .build();
        }
    }
}
