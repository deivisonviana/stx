<?php

namespace Database\Factories;

use App\Models\Record;
use Illuminate\Database\Eloquent\Factories\Factory;
use Faker\Factory as Faker;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Record>
 */
class RecordFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var string
     */
    protected $model = Record::class;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {        
        return [
            'date_hour'   => fake()->dateTimeBetween('-20 years', 'now', 'America/Sao_Paulo'),
            'instant'     => fake()->randomFloat(),
            'maximun'     => fake()->randomFloat(),
            'minimun'     => fake()->randomFloat(),
            'average'     => fake()->randomFloat(),
            'id_station'  => fake()->randomElement(range(1, 7)),
            'id_variable' => fake()->randomElement(range(1, 15)),
            'id_flag'     => fake()->randomElement(range(1, 7))
        ];
    }
    
    /**
     * Generate random meteorological data in a definited range
     *
     * @param int $min
     * @param int $max
     * 
     * @return array<mixed>
     */
    protected function randomFloat(int $min, int $max): array {
        // Create a Faker instance
        $faker = Faker::create();
        
        $inst = $faker->randomFloat(2, $min, $max);

        $maxi = $inst > $min ? $faker->randomFloat(2, $inst, $max) : $max;
        $mini = $inst < $max ? $faker->randomFloat(2, $min, $inst) : $min;

        $medi = ($maxi + $mini) / 2;

        return [$inst, $maxi, $mini, $medi];
    }

    /**
     * Defines the temperatura range state
     *
     * @return Factory
     */
    public function temperature(): Factory {
        return $this->state(function (array $attributes) {
            // Max and Min values
            $min = 22;
            $max = 33;

            $meditions = self::randomFloat($min, $max);

            return [
                'instant'     => $meditions[0],
                'maximun'     => $meditions[1],
                'minimun'     => $meditions[2],
                'average'     => $meditions[3],
                'id_variable' => 2 
            ];
        });
    }

    /**
     * Defines the preasure range state
     *
     * @return Factory
     */
    public function preasure(): Factory {
        return $this->state(function (array $attributes) {
            // Max and Min values
            $min = 900;
            $max = 1000;
            
            $meditions = self::randomFloat($min, $max);

            return [
                'instant'     => $meditions[0],
                'maximun'     => $meditions[1],
                'minimun'     => $meditions[2],
                'average'     => $meditions[3],
                'id_variable' => 7 
            ];
        });
    }

    /**
     * Defines the wind direction state
     *
     * @return Factory
     */
    public function wind_direction(): Factory {
        return $this->state(function (array $attributes) {
            // Max and Min values
            $min = 0;
            $max = 360;
            
            $meditions = self::randomFloat($min, $max);

            return [
                'instant'     => $meditions[0],
                'maximun'     => $meditions[1],
                'minimun'     => $meditions[2],
                'average'     => $meditions[3],
                'id_variable' => 13 
            ];
        });
    }

    /**
     * Defines the wind speed state
     *
     * @return Factory
     */
    public function wind_speed(): Factory {
        return $this->state(function (array $attributes) {
            // Max and Min values
            $min = 0;
            $max = 50;
            
            $meditions = self::randomFloat($min, $max);

            return [
                'instant'     => $meditions[0],
                'maximun'     => $meditions[1],
                'minimun'     => $meditions[2],
                'average'     => $meditions[3],
                'id_variable' => 14 
            ];
        });
    }

    /**
     * Defines the precipitation state
     *
     * @return Factory
     */
    public function precipitation(): Factory {
        return $this->state(function (array $attributes) {
            // Max and Min values
            $min = 0;
            $max = 5;
            
            $meditions = self::randomFloat($min, $max);

            return [
                'instant'     => $meditions[0],
                'maximun'     => $meditions[1],
                'minimun'     => $meditions[2],
                'average'     => $meditions[3],
                'id_variable' => 15
            ];
        });
    }
}
