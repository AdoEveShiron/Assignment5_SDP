package strategy;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        double distance = readDistance(args);

        Navigator navigator = new Navigator(new CarStrategy());
        System.out.println(navigator.plan(distance));

        navigator.setStrategy(new WalkStrategy());
        System.out.println(navigator.plan(distance));

        navigator.setStrategy(new CycleStrategy());
        System.out.println(navigator.plan(distance));
    }

    private static double readDistance(String[] args) {
        if (args.length == 1) {
            return Double.parseDouble(args[0]);
        }
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter distance in km:");
        String line = scanner.nextLine().trim();
        return Double.parseDouble(line);
    }
}
