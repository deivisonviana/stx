<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Manufacter extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'manufacters';

    /**
     * The attributes that are mass assignable.
     *
     * @var array<string>
     */
    protected $fillable = [
        'name',
    ];
}
