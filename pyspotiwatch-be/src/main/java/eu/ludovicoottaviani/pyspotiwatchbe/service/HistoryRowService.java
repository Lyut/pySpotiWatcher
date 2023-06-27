package eu.ludovicoottaviani.pyspotiwatchbe.service;

import eu.ludovicoottaviani.pyspotiwatchbe.model.HistoryRow;
import eu.ludovicoottaviani.pyspotiwatchbe.repository.HistoryRowRepository;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;

@Service
public class HistoryRowService {

    @Autowired
    private HistoryRowRepository historyRowRepository;

    public List<HistoryRow> findAll() {
        return historyRowRepository.findAllByOrderByIdDesc();
    }

    public void insert(HistoryRow row) {
        historyRowRepository.save(row);
    }

    public void delete(String id) {
        historyRowRepository.deleteHistoryRowById(id);
    }


}
