<?php

namespace App\Models;

use DB;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Record extends Model
{
    use HasFactory;

    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'records';

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'date_hour',
        'instant',
        'maximun',
        'minimun',
        'average',
        'id_station',
        'id_variable',
        'id_flag'
    ];

    /**
     * The primary key associated with the table.
     *
     * @var array<string>
     */
    protected $primaryKey = ['id_station', 'id_variable', 'date_hour'];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'date_hour' => 'datetime'
    ];

    /**
     * Indicates if the model's ID is auto-incrementing.
     *
     * @var bool
     */
    public $incrementing = false;

    /**
     * Indicates if the model should be timestamped.
     *
     * @var bool
     */
    public $timestamps = false;

    /**
     * Gets the station that owns the medition
     */
    public function station(): BelongsTo
    {
        return $this->belongsTo(Station::class);
    }

    /**
     * Gets the measure variable
     */
    public function variable(): BelongsTo 
    {
        return $this->belongsTo(Variable::class);
    }

    /**
     * Gets the quality flag
     */
    public function flag(): BelongsTo
    {
        return $this->belongsTo(Flag::class);
    }

    /**
     * Define as chaves primárias compostas para consultas de salvamento.
     *
     * @param \Illuminate\Database\Eloquent\Builder $query
     * @return \Illuminate\Database\Eloquent\Builder
     */
    protected function setKeysForSaveQuery($query)
    {
        $query->where('id_station',  '=', $this->getAttribute('id_station'))
              ->where('id_variable', '=', $this->getAttribute('id_variable'))
              ->where('date_hour',   '=', $this->getAttribute('date_hour'));

        return $query;
    }

    /**
     * Find a record by composite key.
     *
     * @param string $id_station
     * @param string $date_hour
     * @param string $instant
     * 
     * @return \Illuminate\Database\Eloquent\Model|null
     */
    public static function findByCompositeKey($id_station, $date_hour, $instant)
    {
        return static::where([
            ['id_station', '=', $id_station],
            ['date_hour', '=', $date_hour],
            ['instant', '=', $instant],
        ])->first();
    }

    /**
     * Undocumented function
     *
     * @param string $code   Station code
     * @param array $between Date interval
     * @return
     */
    public static function getBruteData(string $code, array $between)
    {
       
        return DB::table('records as r')
            ->where('r.id_station', '=', $code)
            ->where('r.id_variable', '=', 2)
            ->whereBetween('r.date_hour', [$between['start'], $between['end']])
            ->get();
    }

    /**
     * Undocumented function
     *
     * @param string $code Station code
     * @Param array $between Date interval
     * @return 
     */
    public static function getGraphicsData(string $code, array $between)
    {
        return DB::table('records_graphics as r')
            ->where('r.id_station', '=', $code)
            ->whereBetween('r.date', [$between['start'], $between['end']])
            ->orderBy('r.date')
            ->get();
            
    }
}