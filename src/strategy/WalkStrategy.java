package strategy;

public class WalkStrategy implements RouteStrategy {

    private static final double SPEED_KMH = 5;

    @Override
    public String planRoute(double distanceKm) {
        double hours = distanceKm / SPEED_KMH;
        return String.format("Walk: %.1f km, about %.2f h at %.0f km/h", distanceKm, hours, SPEED_KMH);
    }
}
