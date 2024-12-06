-- theft took place on July 28, 2023 on Humphrey Street
-- read crime scene reports
SELECT id, description
FROM crime_scene_reports
WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

--id 295 and 297
-- | 295 | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |
-- | 297 | Littering took place at 16:36. No known witnesses.   [UNLIKELY RELEVANT]
-- find the three interviews mentioning the bakery

SELECT id, transcript
FROM interviews
WHERE month = 7 AND transcript LIKE '%bakery%';

-- | 161 | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
-- | 162 | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
-- | 163 | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |

-- find earliest flight out of Fiftyville

SELECT hour, minute
FROM flights
WHERE year = 2023 AND month = 7 AND day = 29 AND origin_airport_id =
(
    SELECT id
    FROM airports
    WHERE city = 'Fiftyville'
)
ORDER BY hour;

--+------+--------+
--| hour | minute |
--+------+--------+
--| 8    | 20     |
--| 9    | 30     |
--| 12   | 15     |
--| 15   | 20     |
--| 16   | 0      |
--+------+--------+

-- flight at 8:20 next day PURCHASED BY ACCOMPLICE
-- find flight id and destination airport

SELECT id, destination_airport_id
FROM flights
WHERE year = 2023 AND month = 7 AND day = 29 AND hour = 8 AND minute = 20 AND origin_airport_id =
(
    SELECT id
    FROM airports
    WHERE city = 'Fiftyville'
);

-- flight id 36 destination airport id 4
-- find destination airport city

SELECT city
FROM airports
WHERE id = 4;

-- escaped to New York City
-- find passenger name with the passport number on flight 36 and license plates at bakery between 10:15 and 10:25 and made phone calls less than a minute with matching bank account from ATM on Leggett Street

SELECT name
FROM people
WHERE id IN
(
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN
    (
        SELECT account_number
        FROM atm_transactions
        WHERE atm_location = 'Leggett Street' AND year = 2023 AND month = 7 AND day = 28
    )
) AND  passport_number IN
(
    SELECT passport_number
    FROM passengers
    WHERE flight_id = 36
) AND license_plate IN
(
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25
) AND phone_number IN
(
    SELECT caller
    FROM phone_calls
    WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60
);

-- it was Bruce
-- called someone for less than a minute
-- find receiver

SELECT name
FROM people
WHERE phone_number = (
    SELECT receiver
    FROM phone_calls
    WHERE caller = (
        SELECT phone_number
        FROM people
        WHERE name = 'Bruce'
    ) AND year = 2023 AND month = 7 AND day = 28 AND duration < 60
);

-- Accomplice was Robin!
