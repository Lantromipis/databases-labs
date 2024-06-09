package ru.ifmo.se;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import ru.ifmo.se.model.DeliverymanDto;

import java.io.InputStream;
import java.util.List;

@Path("/api/deliveryman")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class DeliverymanResource {

    @Inject
    ObjectMapper objectMapper;

    @GET
    public Response getDelivery(@QueryParam("limit") Integer limit,
                                @QueryParam("offset") Integer offset) throws Exception {

        try (InputStream inputStream = this.getClass().getClassLoader().getResourceAsStream("deliveryman.json")) {
            List<DeliverymanDto> dtos = objectMapper.readValue(inputStream, new TypeReference<List<DeliverymanDto>>() {
            });

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
