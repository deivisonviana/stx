<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class TypeStation extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'type_stations';

    /**
     * The attributes that are mass assignable.
     *
     * @var array<string>
     */
    protected $fillable = [
        'type',
    ];
}
