<?php

use App\Http\Controllers\Api\RecordController;

Route::middleware('interval')->group(function() {

    Route::get('/records/products/{code}/{start}/{end}', [RecordController::class, 'selectProducts'])
        ->name('records.products');

    Route::get('/records/{code}/{start}/{end}', [RecordController::class, 'selectRecords'])
        ->name('records.meteorology');
});

Route::apiResource('/records', RecordController::class);
