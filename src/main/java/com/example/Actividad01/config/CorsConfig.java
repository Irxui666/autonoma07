package com.example.Actividad01.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    private final String[] origenes;
    public CorsConfig(
        @Value(
                "${app.cors.allowed-origins:http://localhost:4200,http://127.0.0.1:4200}") String[] origenes){
        this.origenes = origenes;
    }


    @Override
    public void addCorsMappings(CorsRegistry registry) {
        WebMvcConfigurer.super.addCorsMappings(registry);
        registry.addMapping("/api/**")
                .allowedOrigins(origenes)
                .allowedMethods(
                        "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"
                )
                .allowedHeaders(
                        "Content-Type",
                        "Accept",
                        "Authorization",
                        "Origin"
                )
                .exposedHeaders("Location")
                .allowCredentials(true)
                .maxAge(3600);
    }
}
