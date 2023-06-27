import {Component, OnInit, Pipe, PipeTransform} from '@angular/core';
import {HistoryService} from '../../service/historyservice';
import {HistoryRowDTO} from "../../dto/historyrow";

@Pipe({
  name: 'join'
})
export class JoinPipe implements PipeTransform {
  transform(input: Array<any>, sep = ', '): string {
    return input.map((a) => a.name).join(sep);
  }
}

@Component({
  selector: 'app-historyview',
  templateUrl: './historyview.component.html',
  styleUrls: ['./historyview.component.css']
})
export class HistoryviewComponent implements OnInit {

  historyRows: HistoryRowDTO[];
  a: object;

  constructor(private service: HistoryService) {
  }

  ngOnInit() {
    this.service.getAll().subscribe((r: any) => {
      this.historyRows = r;
    });
  }

  onDelete(id: string) {
    this.service.delete(id).subscribe( d => this.ngOnInit());
  }

}
