package strategy;

public class CarStrategy implements RouteStrategy {

    private static final double SPEED_KMH = 60;

    @Override
    public String planRoute(double distanceKm) {
        double hours = distanceKm / SPEED_KMH;
        return String.format("Car: %.1f km, about %.2f h at %.0f km/h", distanceKm, hours, SPEED_KMH);
    }
}
