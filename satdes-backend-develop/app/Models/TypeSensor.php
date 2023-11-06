<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class TypeSensor extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'type_sensors';

    /**
     * The attributes that are mass assignable.
     *
     * @var array<string>
     */
    protected $fillable = [
        'model_name',
        'model_number',
        'id_manufactor'
    ];
}
