/**
 * Classe DTO di HistoryRow
 */
export class HistoryRowDTO {

  id: string;

  time: Date;

  items: {
    artists: [
      { name: string }
    ]
    album: {
      images: [{ url: string }]
      name: string,
      total_tracks: number
    },
    duration_ms: number,
    track_number: number,
    name: string
  }


}

