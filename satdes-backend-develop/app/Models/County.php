<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class County extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'conties';

    /**
     * The attributes that are mass assignable.
     *
     * @var array<string>
     */
    protected $fillable = [
        'name',
        'id_state'
    ];

    /**
     * Define o relacionamento com a tabela 'estados'
     */
    public function state(): BelongsTo
    {
        return $this->belongsTo(State::class);
    }
}
