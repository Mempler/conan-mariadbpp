#include <iostream>
#include <mariadb++/account.hpp>
#include <mariadb++/connection.hpp>
#include <mariadb++/exceptions.hpp>

void main() {
    try {
        mariadb::account_ref acc = mariadb::account::create("localhost", "root", "", "test", 3306); // We dont care if this fails, we just need to know if linking was successfully.
        auto connection = mariadb::connection::create(acc);
        if (!connection->connected())
            connection->connect();
    } catch (mariadb::exception::connection& ex) {
        std::cout << "an MySQL Error occurred: " + std::string(ex.what()) << std::endl;
    }
}