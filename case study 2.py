class Vehicle:
    def __init__(self, mpg, vin):
        self.mpg = mpg
        self.vin = vin
        self.reserved = False

    def get_description(self):
        return f"MPG: {self.mpg}, VIN: {self.vin}"

    def is_reserved(self):
        return self.reserved

    def set_reserved(self, reserved):
        self.reserved = reserved


class Car(Vehicle):
    def __init__(self, mpg, vin, num_passengers, num_doors):
        super().__init__(mpg, vin)
        self.num_passengers = num_passengers
        self.num_doors = num_doors

    def get_description(self):
        return super().get_description() + f", Passengers: {self.num_passengers}, Doors: {self.num_doors}"


class Van(Vehicle):
    def __init__(self, mpg, vin, num_passengers):
        super().__init__(mpg, vin)
        self.num_passengers = num_passengers

    def get_description(self):
        return super().get_description() + f", Passengers: {self.num_passengers}"


class Truck(Vehicle):
    def __init__(self, mpg, vin, length, num_rooms):
        super().__init__(mpg, vin)
        self.length = length
        self.num_rooms = num_rooms

    def get_description(self):
        return super().get_description() + f", Length: {self.length}, Rooms: {self.num_rooms}"


class Vehicles:
    def __init__(self):
        self.vehicle_list = []

    def add_vehicle(self, vehicle):
        self.vehicle_list.append(vehicle)

    def get_vehicle(self, vin):
        for vehicle in self.vehicle_list:
            if vehicle.vin == vin:
                return vehicle
        return None

    def num_avail_vehicles(self, vehicle_type):
        count = 0
        for vehicle in self.vehicle_list:
            if not vehicle.is_reserved() and isinstance(vehicle, vehicle_type):
                count += 1
        return count

    def get_avail_vehicles(self, vehicle_type):
        available_vehicles = []
        for vehicle in self.vehicle_list:
            if not vehicle.is_reserved() and isinstance(vehicle, vehicle_type):
                available_vehicles.append(vehicle)
        return available_vehicles

    def unreserve_vehicle(self, vin):
        vehicle = self.get_vehicle(vin)
        if vehicle:
            vehicle.set_reserved(False)


class Reservation:
    def __init__(self, name, address, credit_card, vin):
        self.name = name
        self.address = address
        self.credit_card = credit_card
        self.vin = vin

    def get_name(self):
        return self.name

    def get_addr(self):
        return self.address

    def get_credit_card(self):
        return self.credit_card

    def get_vin(self):
        return self.vin


class Reservations:
    def __init__(self):
        self.reservation_list = []

    def is_reserved(self, vin):
        for reservation in self.reservation_list:
            if reservation.vin == vin:
                return True
        return False

    def find_reservation(self, name, addr):
        for reservation in self.reservation_list:
            if reservation.name == name and reservation.address == addr:
                return reservation
        return None

    def get_vin_for_reserv(self, credit_card):
        for reservation in self.reservation_list:
            if reservation.credit_card == credit_card:
                return reservation.vin
        return None

    def add_reservation(self, reservation):
        self.reservation_list.append(reservation)

    def cancel_reservation(self, credit_card):
        for reservation in self.reservation_list:
            if reservation.credit_card == credit_card:
                self.reservation_list.remove(reservation)


class VehicleCost:
    def __init__(self, daily_rate, weekly_rate, weekend_rate, free_miles, per_mile_charge, insur_rate):
        self.daily_rate = daily_rate
        self.weekly_rate = weekly_rate
        self.weekend_rate = weekend_rate
        self.free_miles = free_miles
        self.per_mile_charge = per_mile_charge
        self.insur_rate = insur_rate

    def get_daily_rate(self):
        return self.daily_rate

    def get_weekly_rate(self):
        return self.weekly_rate

    def get_weekend_rate(self):
        return self.weekend_rate

    def get_free_daily_miles(self):
        return self.free_miles

    def get_per_mile_charge(self):
        return self.per_mile_charge

    def get_insurance_rate(self):
        return self.insur_rate


class VehicleCosts:
    def __init__(self, vehicle_types):
        self.costs = vehicle_types
        self.vehicle_types = vehicle_types

    def get_vehicle_cost(self, vehicle_type):
        return self.costs.get(vehicle_type, "Vehicle type not found")

    def add_vehicle_cost(self, veh_type, veh_cost):
        self.costs[veh_type] = veh_cost

    def calc_rental_cost(self, vehicle_type, rental_period, want_insurance, miles_driving):
        cost = 0
        # print(vehicle_type, self.costs)
        if vehicle_type in self.costs:
            if rental_period == "daily":
                cost = float(self.costs[vehicle_type].get_daily_rate())
            elif rental_period == "weekly":
                cost = float(self.costs[vehicle_type].get_weekly_rate())
            elif rental_period == "weekend":
                cost = float(self.costs[vehicle_type].get_weekend_rate())
            cost += max(0, float(miles_driving) - float(self.costs[vehicle_type].get_free_daily_miles())) * float(self.costs[vehicle_type].get_per_mile_charge())
            
            if want_insurance:
                cost += float(self.costs[vehicle_type].get_insurance_rate())
        
        return cost

class SystemInterface:
    def __init__(self, vehicles, reservations, vehicle_costs):
        self.vehicles = vehicles
        self.reservations = reservations
        self.vehicle_costs = vehicle_costs

    def num_avail_vehicles(self, vehicle_type):
        return self.vehicles.num_avail_vehicles(vehicle_type)

    def get_vehicle(self, vin):
        return self.vehicles.get_vehicle(vin)

    def get_vehicle_types(self):
        return self.vehicle_costs.vehicle_types

    def get_vehicle_costs(self, vehicle_type):
        return self.vehicle_costs.get_vehicle_cost(vehicle_type)

    def get_avail_vehicles(self, vehicle_type):
        return self.vehicles.get_avail_vehicles(vehicle_type)

    def is_reserved(self, vin):
        return self.reservations.is_reserved(vin)

    def find_reservation(self, name, addr):
        return self.reservations.find_reservation(name, addr)

    def get_vin_for_reserv(self, credit_card):
        return self.reservations.get_vin_for_reserv(credit_card)

    def add_reservation(self, reservation):
        self.reservations.add_reservation(reservation)

    def cancel_reservation(self, credit_card):
        self.reservations.cancel_reservation(credit_card)

    def calc_rental_cost(self, vehicle_type, rental_period, want_insurance, miles_driving):
        return self.vehicle_costs.calc_rental_cost(vehicle_type, rental_period, want_insurance, miles_driving)


def display_menu():
    print("<<< MAIN MENU >>>")
    print("1. Display Vehicle types")
    print("2. Check Rental rates")
    print("3. Check Available vehicles")
    print("4. Get the cost of a specific rental")
    print("5. Make a reservation")
    print("6. Cancel a reservation")
    print("7. Quit")


def main():
    # Initialize the system components
    vehicles = Vehicles()
    reservations = Reservations()
    car_costs = VehicleCost("50", "300", "100", "100", "0.25", "10")
    van_costs = VehicleCost("60", "350", "120", "120", "0.30", "12")
    truck_costs = VehicleCost("40", "250", "90", "80", "0.20", "8")
    vehicle_costs = VehicleCosts({"Car": car_costs, "Van": van_costs, "Truck": truck_costs})
    system_interface = SystemInterface(vehicles, reservations, vehicle_costs)

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            vehicle_types = system_interface.get_vehicle_types()
            print("Available Vehicle types:")
            for vehicle_type in vehicle_types:
                print(vehicle_type)
        
        elif choice == '2':
            vehicle_type = input("Enter vehicle type (Car/Van/Truck): ")
            costs = system_interface.get_vehicle_costs(vehicle_type)
            if costs != "Vehicle type not found":
                print(f"Rental rates for {vehicle_type}:")
                print("Daily Rate:", costs.get_daily_rate())
                print("Weekly Rate:", costs.get_weekly_rate())
                print("Weekend Rate:", costs.get_weekend_rate())
                print("Free Daily Miles:", costs.get_free_daily_miles())
                print("Per Mile Charge:", costs.get_per_mile_charge())
                print("Insurance Rate:", costs.get_insurance_rate())
            else:
                print("Vehicle type not found")

        elif choice == '3':
            vehicle_type = input("Enter vehicle type (Car/Van/Truck): ")
            num_available = system_interface.num_avail_vehicles(globals()[vehicle_type])
            print(f"Number of available {vehicle_type}s: {num_available}")

        elif choice == '4':
            vehicle_type = input("Enter vehicle type (Car/Van/Truck): ")
            rental_period = input("Enter rental period (daily/weekly/weekend): ")
            want_insurance = input("Do you want insurance? (yes/no): ").lower() == 'yes'
            miles_driving = int(input("Enter miles driving: "))
            cost = system_interface.calc_rental_cost(vehicle_type, rental_period, want_insurance, miles_driving)
            print("Estimated cost:", cost)

        elif choice == '5':
            name = input("Enter name: ")
            address = input("Enter address: ")
            credit_card = input("Enter credit card number: ")
            vin = input("Enter VIN: ")
            reservation = Reservation(name, address, credit_card, vin)
            system_interface.add_reservation(reservation)
            print("Reservation made successfully!")

        elif choice == '6':
            credit_card = input("Enter credit card number to cancel reservation: ")
            system_interface.cancel_reservation(credit_card)
            print("Reservation canceled successfully!")

        elif choice == '7':
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
