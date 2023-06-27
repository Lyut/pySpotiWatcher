package eu.ludovicoottaviani.pyspotiwatchbe.repository;

import eu.ludovicoottaviani.pyspotiwatchbe.model.HistoryRow;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface HistoryRowRepository extends MongoRepository<HistoryRow, String> {

    List<HistoryRow> findAllByOrderByIdDesc();

    void deleteHistoryRowById(String id);

}