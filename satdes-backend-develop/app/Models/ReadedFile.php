<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class ReadedFile extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'readed_files';

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'file',
        'data_read',
        'date_make',
        'id_station'
    ];

    /**
     * Indicates if the model should be timestamped.
     *
     * @var bool
     */
    public $timestamps = false;

    /**
     * Undocumented function
     *
     * @param \Spatie\QueryBuilder\QueryBuilder $query
     */
    public static function registeredData($query) {
        return $query->select(
            'stations.id', 
            'stations.name', 
            'readed_files.file', 
            'readed_files.date_make',
            'readed_files.date_read'
            )
        ->join('stations', 'stations.id', '=', 'readed_files.id_station')
        ->get();
    }
}
