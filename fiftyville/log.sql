-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Crime scene reports with related date: Theft ID is 295
SELECT * FROM crime_scene_reports
WHERE day = 28 AND month = 7 AND year = 2021;

-- Witness information: three witnesses
SELECT * FROM interviews
WHERE day = 28 AND month = 7 AND year = 2021;

-- Witness: drove away within 10 mins of theft
SELECT bakery_security_logs.activity, bakery_security_logs.license_plate, people.name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2021
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute > 15
AND bakery_security_logs.minute < 25;

-- Witness: atm withdrawal from Legget Street
SELECT people.name, atm_transactions.transaction_type FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.transaction_type = 'withdraw'
AND atm_transactions.year = 2021
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_location = 'Leggett Street';

-- Witness: First flight next day. Flight ID = 36, destination id = 4 = LaGuardia, NYC. Passengers from flight
SELECT destination_airport_id FROM flights
WHERE day = 29 AND month = 7
AND year = 2021
ORDER BY hour ASC limit 1;

SELECT city FROM airports
WHERE id = 4;

SELECT name FROM people
WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);

-- Calls under 60 seconds
SELECT people.name, phone_calls.caller FROM people
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE duration < 60
AND phone_calls.day = 28
AND phone_calls.month = 7
AND phone_calls.year = 2021;

-- Only person present in all tables is Bruce

-- Check relevant calls where caller is Bruce

SELECT * FROM phone_calls
WHERE duration < 60
AND caller = '(367) 555-5533'
AND day = 28
AND month = 7
AND year = 2021;

-- Check receiver to see accomplice

SELECT name FROM people
WHERE phone_number = '(375) 555-8161';
