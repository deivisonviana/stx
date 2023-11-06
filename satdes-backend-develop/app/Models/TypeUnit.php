<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class TypeUnit extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'type_units';

    /**
     * The attributes that are mass assignable.
     *
     * @var array<string>
     */
    protected $fillable = [
        'acronym',
        'measure'
    ];
}
