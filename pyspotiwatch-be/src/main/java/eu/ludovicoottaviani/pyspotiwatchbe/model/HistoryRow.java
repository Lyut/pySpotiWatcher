package eu.ludovicoottaviani.pyspotiwatchbe.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;


@Document("history")
@Data
public class HistoryRow {

    @Id
    private String id;

    private Object time;

    private Object items;
}
