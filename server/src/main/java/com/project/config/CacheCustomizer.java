//package com.project.config;
//
//import org.springframework.boot.autoconfigure.cache.CacheManagerCustomizer;
//import org.springframework.cache.concurrent.ConcurrentMapCacheManager;
//import org.springframework.stereotype.Component;
//
//import java.util.Arrays;
//
//@Component
//public class CacheCustomizer implements CacheManagerCustomizer<ConcurrentMapCacheManager> {
//
//    @Override
//    public void customize(ConcurrentMapCacheManager cacheManager) {
//        cacheManager.setCacheNames(Arrays.asList("p1", "p2"));
//    }
//}
